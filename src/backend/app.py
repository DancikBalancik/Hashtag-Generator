from flask import Flask, request, jsonify
import os
import json
import requests

app = Flask(__name__)

# --- Hashtag logic (moved from old GUI) ---
SETTINGS_PATH = os.path.expanduser('~/.hashtag_generator_settings.json')
HISTORY_PATH = os.path.expanduser('~/.hashtag_generator_history.json')

def load_settings():
    if os.path.exists(SETTINGS_PATH):
        with open(SETTINGS_PATH, 'r') as f:
            return json.load(f)
    return {
        "remove_special_chars": False,
        "capitalization_mode": "first",
        "history_max_items": 10,
        "theme": "light",
        "character_limit": 0
    }

def save_settings(settings):
    with open(SETTINGS_PATH, 'w') as f:
        json.dump(settings, f)

def load_history():
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, 'r') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_PATH, 'w') as f:
        json.dump(history, f)

def generate_hashtag(text, settings):
    if not text:
        return ""
    if settings.get("remove_special_chars"):
        text = ''.join(c for c in text if c.isalnum() or c.isspace())
    mode = settings.get("capitalization_mode", "first")
    if mode == "first":
        text = text.title()
    elif mode == "all_caps":
        text = text.upper()
    elif mode == "lowercase":
        text = text.lower()
    hashtag = "#" + text.replace(" ", "")
    return hashtag

@app.route('/api/hashtag', methods=['POST'])
def api_generate_hashtag():
    data = request.json
    text = data.get('text', '')
    settings = load_settings()
    hashtag = generate_hashtag(text, settings)
    # Update history
    history = load_history()
    if hashtag and hashtag not in history:
        history.insert(0, hashtag)
        history = history[:settings.get('history_max_items', 10)]
        save_history(history)
    return jsonify({'hashtag': hashtag})

@app.route('/api/history', methods=['GET'])
def api_get_history():
    return jsonify({'history': load_history()})

@app.route('/api/settings', methods=['GET', 'POST'])
def api_settings():
    if request.method == 'POST':
        settings = request.json
        save_settings(settings)
        return jsonify({'status': 'ok'})
    return jsonify(load_settings())

# --- LLM Provider Registry ---
LLM_PROVIDERS = [
    {
        'id': 'openai',
        'name': 'OpenAI',
        'models': ['gpt-3.5-turbo', 'gpt-4', 'text-davinci-003'],
        'api_key_label': 'OpenAI API Key',
        'extra_fields': []
    },
    {
        'id': 'anthropic',
        'name': 'Anthropic Claude',
        'models': ['claude-3-opus-20240229', 'claude-3-sonnet-20240229'],
        'api_key_label': 'Anthropic API Key',
        'extra_fields': []
    },
    {
        'id': 'azure',
        'name': 'Azure OpenAI',
        'models': ['gpt-35-turbo', 'gpt-4'],
        'api_key_label': 'Azure API Key',
        'extra_fields': ['endpoint']
    },
    {
        'id': 'gemini',
        'name': 'Google Gemini',
        'models': ['gemini-pro'],
        'api_key_label': 'Gemini API Key',
        'extra_fields': []
    },
    {
        'id': 'mistral',
        'name': 'Mistral AI',
        'models': ['mistral-tiny', 'mistral-small', 'mistral-medium', 'mistral-large'],
        'api_key_label': 'Mistral API Key',
        'extra_fields': []
    },
    {
        'id': 'huggingface',
        'name': 'HuggingFace Inference API',
        'models': ['bigscience/bloom', 'meta-llama/Llama-2-7b-chat-hf'],
        'api_key_label': 'HuggingFace API Key',
        'extra_fields': ['model']
    },
    {
        'id': 'ollama',
        'name': 'Ollama (local)',
        'models': ['llama2', 'mistral', 'phi', 'codellama'],
        'api_key_label': None,
        'extra_fields': ['model', 'base_url']
    },
    {
        'id': 'lmstudio',
        'name': 'LM Studio (local)',
        'models': ['any'],
        'api_key_label': None,
        'extra_fields': ['model', 'base_url']
    },
]

@app.route('/api/providers', methods=['GET'])
def api_providers():
    return jsonify({'providers': LLM_PROVIDERS})

@app.route('/api/models', methods=['GET'])
def api_models():
    provider_id = request.args.get('provider')
    api_key = request.args.get('api_key')
    endpoint = request.args.get('endpoint')
    base_url = request.args.get('base_url')
    # Dynamic model fetching logic
    if provider_id == 'openai' and api_key:
        url = 'https://api.openai.com/v1/models'
        headers = {'Authorization': f'Bearer {api_key}'}
        r = requests.get(url, headers=headers)
        if r.ok:
            data = r.json()
            models = [m['id'] for m in data.get('data', [])]
            return jsonify({'models': models})
        return jsonify({'models': []})
    elif provider_id == 'huggingface' and api_key:
        # HuggingFace does not have a public list endpoint for all models, so return popular ones
        return jsonify({'models': [
            'bigscience/bloom',
            'meta-llama/Llama-2-7b-chat-hf',
            'tiiuae/falcon-7b-instruct',
            'google/flan-t5-xl',
            'mistralai/Mistral-7B-Instruct-v0.2',
        ]})
    elif provider_id == 'mistral' and api_key:
        url = 'https://api.mistral.ai/v1/models'
        headers = {'Authorization': f'Bearer {api_key}'}
        r = requests.get(url, headers=headers)
        if r.ok:
            data = r.json()
            models = [m['id'] for m in data.get('data', [])]
            return jsonify({'models': models})
        return jsonify({'models': []})
    elif provider_id == 'ollama' and base_url:
        url = f'{base_url.rstrip("/")}/api/tags'
        try:
            r = requests.get(url)
            if r.ok:
                data = r.json()
                models = [m['name'] for m in data.get('models', [])]
                return jsonify({'models': models})
        except Exception:
            pass
        return jsonify({'models': []})
    elif provider_id == 'lmstudio' and base_url:
        url = f'{base_url.rstrip("/")}/v1/models'
        try:
            r = requests.get(url)
            if r.ok:
                data = r.json()
                models = [m['id'] for m in data.get('data', [])]
                return jsonify({'models': models})
        except Exception:
            pass
        return jsonify({'models': []})
    # For other providers, return an empty list or static fallback
    return jsonify({'models': []})

@app.route('/api/ai', methods=['POST'])
def api_ai():
    data = request.json
    provider = data.get('provider')
    prompt = data.get('prompt')
    api_key = data.get('api_key')
    model = data.get('model')
    endpoint = data.get('endpoint')
    base_url = data.get('base_url')
    # Dispatch to correct provider
    if provider == 'openai':
        return openai_completion(prompt, api_key, model)
    elif provider == 'anthropic':
        return anthropic_completion(prompt, api_key, model)
    elif provider == 'azure':
        return azure_openai_completion(prompt, api_key, model, endpoint)
    elif provider == 'gemini':
        return gemini_completion(prompt, api_key, model)
    elif provider == 'mistral':
        return mistral_completion(prompt, api_key, model)
    elif provider == 'huggingface':
        return huggingface_completion(prompt, api_key, model)
    elif provider == 'ollama':
        return ollama_completion(prompt, base_url, model)
    elif provider == 'lmstudio':
        return lmstudio_completion(prompt, base_url, model)
    else:
        return jsonify({'error': 'Unknown provider'}), 400

# --- Provider Implementations ---
def openai_completion(prompt, api_key, model):
    url = 'https://api.openai.com/v1/chat/completions' if model.startswith('gpt') else 'https://api.openai.com/v1/completions'
    headers = {'Authorization': f'Bearer {api_key}'}
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}] if url.endswith('chat/completions') else None,
        'prompt': prompt if url.endswith('completions') else None,
        'max_tokens': 32
    }
    payload = {k: v for k, v in payload.items() if v is not None}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        data = r.json()
        if 'choices' in data:
            return jsonify({'result': data['choices'][0].get('message', {}).get('content', data['choices'][0].get('text', ''))})
    return jsonify({'error': r.text}), 400

def anthropic_completion(prompt, api_key, model):
    url = 'https://api.anthropic.com/v1/messages'
    headers = {'x-api-key': api_key, 'anthropic-version': '2023-06-01'}
    payload = {
        'model': model,
        'max_tokens': 32,
        'messages': [{"role": "user", "content": prompt}]
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        data = r.json()
        return jsonify({'result': data.get('content', data.get('completion', ''))})
    return jsonify({'error': r.text}), 400

def azure_openai_completion(prompt, api_key, model, endpoint):
    if not endpoint:
        return jsonify({'error': 'Azure endpoint required'}), 400
    headers = {'api-key': api_key, 'Content-Type': 'application/json'}
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 32
    }
    r = requests.post(endpoint, headers=headers, json=payload)
    if r.ok:
        data = r.json()
        return jsonify({'result': data['choices'][0]['message']['content']})
    return jsonify({'error': r.text}), 400

def gemini_completion(prompt, api_key, model):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    r = requests.post(url, json=payload)
    if r.ok:
        data = r.json()
        return jsonify({'result': data['candidates'][0]['content']['parts'][0]['text']})
    return jsonify({'error': r.text}), 400

def mistral_completion(prompt, api_key, model):
    url = f'https://api.mistral.ai/v1/chat/completions'
    headers = {'Authorization': f'Bearer {api_key}'}
    payload = {
        'model': model,
        'messages': [{'role': 'user', 'content': prompt}],
        'max_tokens': 32
    }
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        data = r.json()
        return jsonify({'result': data['choices'][0]['message']['content']})
    return jsonify({'error': r.text}), 400

def huggingface_completion(prompt, api_key, model):
    url = f'https://api-inference.huggingface.co/models/{model}'
    headers = {'Authorization': f'Bearer {api_key}'}
    payload = {"inputs": prompt}
    r = requests.post(url, headers=headers, json=payload)
    if r.ok:
        data = r.json()
        if isinstance(data, list) and data:
            return jsonify({'result': data[0].get('generated_text', '')})
        elif isinstance(data, dict):
            return jsonify({'result': data.get('generated_text', '')})
    return jsonify({'error': r.text}), 400

def ollama_completion(prompt, base_url, model):
    url = f'{base_url.rstrip("/")}/api/generate'
    payload = {"model": model, "prompt": prompt}
    try:
        r = requests.post(url, json=payload, timeout=10)
        if r.ok:
            # Ollama may return multiple JSON objects (streaming). Parse only the first.
            text = r.text.strip()
            if text.startswith('{'):
                # If multiple JSON objects, split and parse the first
                first_json = text.split('\n')[0]
                data = json.loads(first_json)
                return jsonify({'result': data.get('response', '')})
            else:
                return jsonify({'error': 'Ollama returned unexpected response format.'}), 400
        else:
            return jsonify({'error': f'Ollama error: {r.status_code} {r.text}'}), 400
    except requests.exceptions.ConnectionError:
        return jsonify({'error': f'Could not connect to Ollama at {url}. Is the Ollama server running and accessible?'}), 400
    except Exception as e:
        return jsonify({'error': f'Ollama request failed: {str(e)}'}), 400

def lmstudio_completion(prompt, base_url, model):
    url = f'{base_url.rstrip("/")}/v1/completions'
    payload = {"model": model, "prompt": prompt, "max_tokens": 32}
    r = requests.post(url, json=payload)
    if r.ok:
        data = r.json()
        return jsonify({'result': data['choices'][0]['text']})
    return jsonify({'error': r.text}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
