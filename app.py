from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import boto3
import json

app = Flask(__name__)
CORS(app)

# Initialize AgentCore Runtime client
runtime_client = boto3.client('bedrock-agentcore')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Call your deployed translator application
        payload_data = json.dumps({
            'prompt': f"Translate to Amharic: {text}"
        }).encode('utf-8')
        
        response = runtime_client.invoke_agent_runtime(
            agentRuntimeArn='arn:aws:bedrock-agentcore:us-east-1:242201304709:runtime/english_amharic_translator-vxxPkP5dFF',
            payload=payload_data
        )
        
        # Extract the translated text from response
        response_body = response['response'].read()
        decoded_response = response_body.decode('utf-8')
        translated_text = json.loads(decoded_response)
        
        return jsonify({'translatedText': translated_text})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)