"""
Flask app for FLUX.2-klein-4B image generation
Generates images at 800x480, saves both original and rotated versions,
with gallery browsing and cleanup functionality
"""

from flask import Flask, request, send_file, url_for, jsonify
from PIL import Image
import torch
from diffusers import Flux2KleinPipeline
import os
import uuid
from datetime import datetime
import shutil
import dspy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Embedded HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FLUX Image Generator for Inky Frame</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .nav {
            max-width: 1200px;
            margin: 0 auto 20px;
            display: flex;
            gap: 10px;
        }
        
        .nav button {
            padding: 12px 24px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            border: 2px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .nav button.active {
            background: #667eea;
            color: white;
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .nav button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            background: white;
        }
        
        .nav button.active:hover {
            background: #5568d3;
            border-color: #5568d3;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px;
        }
        
        .view {
            display: none;
        }
        
        .view.active {
            display: block;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 28px;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 30px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 500;
        }
        
        textarea {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            transition: border-color 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        button {
            padding: 14px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        button:active:not(:disabled) {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .danger-btn {
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        }
        
        .danger-btn:hover:not(:disabled) {
            box-shadow: 0 4px 12px rgba(220, 53, 69, 0.4);
        }
        
        .loader {
            display: none;
            text-align: center;
            margin: 20px 0;
        }
        
        .loader.active {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .result {
            display: none;
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .result.active {
            display: block;
        }
        
        .result h3 {
            color: #333;
            margin-bottom: 15px;
        }
        
        .image-pair {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .image-container {
            text-align: center;
        }
        
        .image-container h4 {
            margin-bottom: 10px;
            color: #555;
            font-size: 14px;
        }
        
        .image-container img {
            width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
        }
        
        .download-btn {
            display: inline-block;
            padding: 8px 16px;
            background: #28a745;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            transition: background 0.3s;
            margin: 5px;
        }
        
        .download-btn:hover {
            background: #218838;
        }
        
        .error {
            display: none;
            padding: 15px;
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            color: #721c24;
            margin-top: 15px;
        }
        
        .error.active {
            display: block;
        }
        
        .success {
            display: none;
            padding: 15px;
            background: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            color: #155724;
            margin-top: 15px;
        }
        
        .success.active {
            display: block;
        }
        
        .info-box {
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 12px;
            margin-bottom: 20px;
            border-radius: 4px;
            font-size: 14px;
            color: #0c5aa6;
        }
        
        .gallery-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .gallery-item {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .gallery-item img {
            width: 100%;
            border-radius: 6px;
            margin-bottom: 10px;
        }
        
        .gallery-item .meta {
            font-size: 12px;
            color: #666;
            margin-bottom: 10px;
        }
        
        .gallery-item .actions {
            display: flex;
            gap: 5px;
            flex-wrap: wrap;
        }
        
        .delete-btn {
            display: inline-block;
            padding: 8px 16px;
            background: #dc3545;
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            transition: background 0.3s;
            margin: 5px;
            border: none;
            cursor: pointer;
        }
        
        .delete-btn:hover {
            background: #c82333;
        }
        
        .gallery-stats {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .stat {
            text-align: center;
        }
        
        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="nav">
        <button onclick="showView('generate')" class="active" id="navGenerate">Generate</button>
        <button onclick="showView('gallery')" id="navGallery">Gallery</button>
        <button onclick="showView('settings')" id="navSettings">Settings</button>
    </div>

    <div class="container">
        <!-- Generate View -->
        <div id="generateView" class="view active">
            <h1>🎨 FLUX Image Generator</h1>
            <p class="subtitle">For Inky Frame 7.3" Display (800×480)</p>
            
            <div class="info-box">
                <strong>Info:</strong> Generates two versions - original (800×480) and rotated for Inky Frame (480×800)
            </div>
            
            <form id="generateForm">
                <div class="form-group">
                    <label for="prompt">Enter your image prompt:</label>
                    <textarea 
                        id="prompt" 
                        name="prompt" 
                        placeholder="Example: A serene mountain landscape at sunset with a lake in the foreground"
                        required
                    ></textarea>
                </div>
                
                <button type="submit" id="generateBtn">
                    🎨 Generate Images
                </button>
            </form>
            
            <div class="loader" id="loader">
                <div class="spinner"></div>
                <p id="loaderText">Starting generation...</p>
                <p id="loaderTime" style="font-size: 12px; color: #999; margin-top: 10px;">Elapsed: <span id="elapsedTime">0s</span></p>
            </div>
            
            <div class="error" id="error"></div>
            
            <div class="result" id="result">
                <h3>✅ Images Generated Successfully!</h3>
                <div class="image-pair">
                    <div class="image-container">
                        <h4>📱 Original (800×480)</h4>
                        <img id="originalImage" src="" alt="Original image">
                        <a href="#" id="downloadOriginal" class="download-btn" download>
                            ⬇️ Download Original
                        </a>
                    </div>
                    <div class="image-container">
                        <h4>🖼️ Inky Frame (480×800)</h4>
                        <img id="rotatedImage" src="" alt="Rotated image for Inky Frame">
                        <a href="#" id="downloadRotated" class="download-btn" download>
                            ⬇️ Download for Inky Frame
                        </a>
                    </div>
                </div>
                <p style="color: #666; font-size: 14px;">
                    <strong>Your prompt:</strong> <span id="userPrompt"></span><br>
                    <strong>Refined prompt:</strong> <span id="refinedPrompt" style="font-style: italic; color: #28a745;"></span><br>
                    <strong>Generated:</strong> <span id="timestamp"></span><br>
                    <strong>Refinement time:</strong> <span id="refinementTime"></span><br>
                    <strong>Generation time:</strong> <span id="generationTime"></span><br>
                    <strong>Total time:</strong> <span id="totalTime"></span>
                </p>
            </div>
        </div>

        <!-- Gallery View -->
        <div id="galleryView" class="view">
            <h1>🖼️ Image Gallery</h1>
            <p class="subtitle">Browse previously generated images</p>
            
            <div class="gallery-stats">
                <div class="stat">
                    <div class="stat-value" id="totalImages">0</div>
                    <div class="stat-label">Image Pairs</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="totalSize">0 MB</div>
                    <div class="stat-label">Total Size</div>
                </div>
                <div style="display: flex; gap: 10px;">
                    <a href="/latest.jpg" class="download-btn" download style="padding: 10px 20px; text-decoration: none;">
                        ⬇️ Latest Image
                    </a>
                    <button onclick="loadGallery()" style="padding: 10px 20px;">
                        🔄 Refresh
                    </button>
                </div>
            </div>
            
            <div id="galleryGrid" class="gallery-grid">
                <p style="text-align: center; color: #666;">Loading...</p>
            </div>
        </div>

        <!-- Settings View -->
        <div id="settingsView" class="view">
            <h1>⚙️ Settings</h1>
            <p class="subtitle">Manage generated images</p>
            
            <div class="info-box">
                <strong>Warning:</strong> Cleanup operations cannot be undone!
            </div>
            
            <div style="margin-top: 30px;">
                <h3 style="margin-bottom: 15px;">Storage Management</h3>
                <p style="color: #666; margin-bottom: 20px;">
                    Images are stored in the <code>generated_images/</code> folder.
                </p>
                
                <button onclick="cleanupImages()" class="danger-btn" id="cleanupBtn">
                    🗑️ Delete All Generated Images
                </button>
                
                <div class="success" id="cleanupSuccess"></div>
                <div class="error" id="cleanupError"></div>
            </div>
        </div>
    </div>
    
    <script>
        let currentView = 'generate';
        
        function showView(view) {
            // Update nav buttons
            document.querySelectorAll('.nav button').forEach(btn => btn.classList.remove('active'));
            document.getElementById('nav' + view.charAt(0).toUpperCase() + view.slice(1)).classList.add('active');
            
            // Update views
            document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
            document.getElementById(view + 'View').classList.add('active');
            
            currentView = view;
            
            // Load gallery when switching to it
            if (view === 'gallery') {
                loadGallery();
            }
        }
        
        // Generate form
        const form = document.getElementById('generateForm');
        const generateBtn = document.getElementById('generateBtn');
        const loader = document.getElementById('loader');
        const result = document.getElementById('result');
        const error = document.getElementById('error');
        const promptInput = document.getElementById('prompt');
        
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const prompt = promptInput.value.trim();
            if (!prompt) return;
            
            // Reset UI
            loader.classList.add('active');
            result.classList.remove('active');
            error.classList.remove('active');
            generateBtn.disabled = true;
            generateBtn.textContent = 'Generating...';
            
            // Start elapsed time counter
            let startTime = Date.now();
            let timerInterval = setInterval(() => {
                const elapsed = Math.floor((Date.now() - startTime) / 1000);
                document.getElementById('elapsedTime').textContent = elapsed + 's';
            }, 1000);
            
            // Update status messages
            document.getElementById('loaderText').textContent = 'Refining prompt with AI...';
            
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prompt: prompt })
                });
                
                // Update status for long-running generation
                setTimeout(() => {
                    if (loader.classList.contains('active')) {
                        document.getElementById('loaderText').textContent = 'Generating image (this may take 30-120s on CPU)...';
                    }
                }, 5000);
                
                const data = await response.json();
                
                // Stop timer
                clearInterval(timerInterval);
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Display results
                document.getElementById('originalImage').src = data.original_url.replace('/download/', '/view/');
                document.getElementById('rotatedImage').src = data.rotated_url.replace('/download/', '/view/');
                document.getElementById('downloadOriginal').href = data.original_url;
                document.getElementById('downloadRotated').href = data.rotated_url;
                document.getElementById('userPrompt').textContent = data.user_prompt;
                document.getElementById('refinedPrompt').textContent = data.refined_prompt;
                document.getElementById('timestamp').textContent = data.timestamp;
                document.getElementById('refinementTime').textContent = data.refinement_time + 's';
                document.getElementById('generationTime').textContent = data.generation_time + 's';
                document.getElementById('totalTime').textContent = data.total_time + 's';
                
                result.classList.add('active');
                
            } catch (err) {
                clearInterval(timerInterval);
                error.textContent = `Error: ${err.message}`;
                error.classList.add('active');
            } finally {
                clearInterval(timerInterval);
                loader.classList.remove('active');
                generateBtn.disabled = false;
                generateBtn.textContent = '🎨 Generate Images';
                // Reset loader text for next time
                document.getElementById('loaderText').textContent = 'Starting generation...';
                document.getElementById('elapsedTime').textContent = '0s';
            }
        });
        
        // Load gallery
        async function loadGallery() {
            const grid = document.getElementById('galleryGrid');
            grid.innerHTML = '<p style="text-align: center; color: #666;">Loading...</p>';
            
            try {
                const response = await fetch('/gallery');
                const data = await response.json();
                
                document.getElementById('totalImages').textContent = data.total_pairs;
                document.getElementById('totalSize').textContent = (data.total_size / 1024 / 1024).toFixed(2) + ' MB';
                
                if (data.images.length === 0) {
                    grid.innerHTML = '<p style="text-align: center; color: #666;">No images generated yet.</p>';
                    return;
                }
                
                grid.innerHTML = '';
                data.images.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'gallery-item';
                    div.id = 'item-' + item.id;
                    div.innerHTML = `
                        <img src="/view/${item.rotated}" alt="Generated image">
                        <div class="meta">
                            <strong>Generated:</strong> ${item.timestamp}<br>
                            <strong>ID:</strong> ${item.id}
                        </div>
                        <div class="actions">
                            <a href="/download/${item.original}" class="download-btn" download>📱 Original</a>
                            <a href="/download/${item.rotated}" class="download-btn" download>🖼️ Inky</a>
                            <button class="delete-btn" onclick="deleteImagePair('${item.id}')">🗑️ Delete</button>
                        </div>
                    `;
                    grid.appendChild(div);
                });
                
            } catch (err) {
                grid.innerHTML = `<p style="text-align: center; color: #dc3545;">Error loading gallery: ${err.message}</p>`;
            }
        }
        
        // Delete individual image pair
        async function deleteImagePair(imageId) {
            if (!confirm('Delete this image pair? This cannot be undone!')) {
                return;
            }
            
            const item = document.getElementById('item-' + imageId);
            if (item) {
                item.style.opacity = '0.5';
            }
            
            try {
                const response = await fetch('/delete/' + imageId, { method: 'DELETE' });
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                // Remove from UI
                if (item) {
                    item.remove();
                }
                
                // Update stats
                const totalImages = document.getElementById('totalImages');
                const totalSize = document.getElementById('totalSize');
                const currentCount = parseInt(totalImages.textContent);
                const currentSize = parseFloat(totalSize.textContent);
                
                totalImages.textContent = currentCount - 1;
                totalSize.textContent = (currentSize - (data.freed_space / 1024 / 1024)).toFixed(2) + ' MB';
                
                // Check if gallery is now empty
                const grid = document.getElementById('galleryGrid');
                if (grid.children.length === 0) {
                    grid.innerHTML = '<p style="text-align: center; color: #666;">No images generated yet.</p>';
                }
                
            } catch (err) {
                alert('Error deleting image: ' + err.message);
                if (item) {
                    item.style.opacity = '1';
                }
            }
        }
        
        // Cleanup images
        async function cleanupImages() {
            const cleanupBtn = document.getElementById('cleanupBtn');
            const cleanupSuccess = document.getElementById('cleanupSuccess');
            const cleanupError = document.getElementById('cleanupError');
            
            if (!confirm('Are you sure you want to delete ALL generated images? This cannot be undone!')) {
                return;
            }
            
            cleanupSuccess.classList.remove('active');
            cleanupError.classList.remove('active');
            cleanupBtn.disabled = true;
            cleanupBtn.textContent = 'Deleting...';
            
            try {
                const response = await fetch('/cleanup', { method: 'POST' });
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                cleanupSuccess.textContent = `✅ Successfully deleted ${data.deleted_count} image pairs (${(data.freed_space / 1024 / 1024).toFixed(2)} MB freed)`;
                cleanupSuccess.classList.add('active');
                
            } catch (err) {
                cleanupError.textContent = `Error: ${err.message}`;
                cleanupError.classList.add('active');
            } finally {
                cleanupBtn.disabled = false;
                cleanupBtn.textContent = '🗑️ Delete All Generated Images';
            }
        }
        
        // Load gallery on page load if on gallery view
        if (currentView === 'gallery') {
            loadGallery();
        }
    </script>
</body>
</html>
"""

# Configuration
OUTPUT_DIR = "generated_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Device configuration
device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32

# Global pipeline variable - will be loaded once at startup
pipe = None

# DSPy configuration for prompt refinement
dspy_lm = None


def init_dspy():
    """Initialize DSPy with local LLM via OpenAI-compatible API"""
    global dspy_lm
    
    try:
        # Get local LLM endpoint from environment
        # Default to localhost Ollama endpoint
        llm_api_base = os.getenv('LLM_API_BASE', 'http://localhost:11434/v1')
        llm_model = os.getenv('LLM_MODEL', 'llama3.2')
        
        print(f"Configuring DSPy with OpenAI-compatible LLM: {llm_model} at {llm_api_base}")
        
        # Configure DSPy with OpenAI-compatible endpoint
        dspy_lm = dspy.LM(
            model=f'openai/{llm_model}',
            api_base=llm_api_base,
            api_key='not-needed'  # Local models don't need keys
        )
        dspy.configure(lm=dspy_lm)
        
        print("✓ DSPy initialized with OpenAI-compatible local LLM for prompt refinement")
        return True
    except Exception as e:
        print(f"⚠️  Failed to initialize DSPy: {e}")
        print("⚠️  Prompt refinement disabled - will use original prompts")
        return False


class PromptRefiner(dspy.Signature):
    """Refine a user's image generation prompt to be more detailed and effective for FLUX image generation."""
    
    user_prompt = dspy.InputField(desc="The user's original image prompt")
    refined_prompt = dspy.OutputField(desc="A refined, detailed prompt optimized for FLUX image generation. Should be concrete, descriptive, include artistic style, lighting, composition details. Keep it focused and under 100 words.")


def refine_prompt(user_prompt):
    """Use DSPy to refine the user's prompt"""
    global dspy_lm
    
    if dspy_lm is None:
        # DSPy not configured, return original prompt
        return user_prompt, 0.0
    
    try:
        import time
        start_time = time.time()
        
        # Use DSPy to refine the prompt
        refiner = dspy.ChainOfThought(PromptRefiner)
        result = refiner(user_prompt=user_prompt)
        
        refinement_time = time.time() - start_time
        
        return result.refined_prompt, refinement_time
    except Exception as e:
        print(f"Error refining prompt: {e}")
        return user_prompt, 0.0


def init_model():
    """Initialize the FLUX model once at startup"""
    global pipe
    print("=" * 60)
    print("Loading FLUX.2-klein-4B model...")
    print(f"Device: {device}")
    print(f"Dtype: {dtype}")
    print("=" * 60)
    
    pipe = Flux2KleinPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=dtype
    )
    
    if device == "cuda":
        pipe.enable_model_cpu_offload()  # Save VRAM
    
    print("✓ Model loaded successfully!")
    print("=" * 60)
    return pipe


def rotate_and_convert(img, quality=70):
    """
    Rotate image 90 degrees counterclockwise (left) and convert to RGB JPG
    
    Args:
        img: PIL Image object
        quality: JPG quality (0-100)
    
    Returns:
        PIL Image object (rotated)
    """
    # Rotate 90 degrees counterclockwise
    rotated = img.rotate(90, expand=True)
    
    # Convert RGBA to RGB if necessary
    if rotated.mode in ('RGBA', 'LA', 'P'):
        rgb_img = Image.new('RGB', rotated.size, (255, 255, 255))
        rgb_img.paste(rotated, mask=rotated.split()[-1] if rotated.mode == 'RGBA' else None)
        rotated = rgb_img
    elif rotated.mode != 'RGB':
        rotated = rotated.convert('RGB')
    
    return rotated


@app.route('/')
def index():
    """Render the main page"""
    return HTML_TEMPLATE


@app.route('/generate', methods=['POST'])
def generate_image():
    """Generate image from prompt - saves both original and rotated versions"""
    global pipe
    
    if pipe is None:
        return jsonify({'error': 'Model not loaded. Please restart the server.'}), 503
    
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '').strip()
        
        if not user_prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Start timing
        import time
        start_time = time.time()
        
        # Refine the prompt using DSPy
        print(f"Original prompt: {user_prompt}")
        refined_prompt, refinement_time = refine_prompt(user_prompt)
        print(f"Refined prompt: {refined_prompt}")
        print(f"Refinement took: {refinement_time:.2f}s")
        
        # Use the refined prompt for generation
        prompt_to_use = refined_prompt
        
        # Generate unique ID for this image pair
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        base_filename = f"{timestamp}_{unique_id}"
        
        original_filename = f"{base_filename}_original.jpg"
        rotated_filename = f"{base_filename}_inky.jpg"
        
        original_path = os.path.join(OUTPUT_DIR, original_filename)
        rotated_path = os.path.join(OUTPUT_DIR, rotated_filename)
        
        # Generate image at 800x480 (portrait orientation)
        print(f"Generating image for prompt: {prompt_to_use}")
        generation_start = time.time()
        
        # Use random seed for varied results
        seed = torch.randint(0, 2**32, (1,)).item()
        print(f"Using seed: {seed}")
        
        image = pipe(
            prompt=prompt_to_use,
            height=800,
            width=480,
            guidance_scale=4.0,  # Increased from 1.0 for better quality
            num_inference_steps=4,
            generator=torch.Generator(device=device).manual_seed(seed)
        ).images[0]
        generation_time = time.time() - generation_start
        
        # Save original image
        original_rgb = image.convert('RGB') if image.mode != 'RGB' else image
        original_rgb.save(original_path, 'JPEG', quality=70, optimize=True)
        print(f"Original saved: {original_path} ({original_rgb.size})")
        
        # Rotate 90 degrees left (800x480 -> 480x800) for Inky Frame
        rotate_start = time.time()
        rotated_image = rotate_and_convert(image, quality=70)
        rotated_image.save(rotated_path, 'JPEG', quality=70, optimize=True)
        rotate_time = time.time() - rotate_start
        print(f"Rotated saved: {rotated_path} ({rotated_image.size})")
        
        # Calculate total time
        total_time = time.time() - start_time
        
        print(f"Refinement: {refinement_time:.2f}s, Generation: {generation_time:.2f}s, Rotation: {rotate_time:.2f}s, Total: {total_time:.2f}s")
        
        # Return URLs for both images
        original_url = url_for('download_image', filename=original_filename)
        rotated_url = url_for('download_image', filename=rotated_filename)
        
        return jsonify({
            'success': True,
            'original_url': original_url,
            'rotated_url': rotated_url,
            'original_filename': original_filename,
            'rotated_filename': rotated_filename,
            'original_size': original_rgb.size,
            'rotated_size': rotated_image.size,
            'timestamp': timestamp,
            'user_prompt': user_prompt,
            'refined_prompt': refined_prompt,
            'refinement_time': round(refinement_time, 2),
            'generation_time': round(generation_time, 2),
            'rotation_time': round(rotate_time, 2),
            'total_time': round(total_time, 2)
        })
        
    except Exception as e:
        print(f"Error generating image: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/download/<filename>')
def download_image(filename):
    """Download generated image"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg', as_attachment=True)
    else:
        return "File not found", 404


@app.route('/view/<filename>')
def view_image(filename):
    """View generated image in browser"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        return send_file(filepath, mimetype='image/jpeg')
    else:
        return "File not found", 404


@app.route('/gallery')
def gallery():
    """Get list of all generated images"""
    try:
        if not os.path.exists(OUTPUT_DIR):
            return jsonify({'images': [], 'total_pairs': 0, 'total_size': 0})
        
        files = os.listdir(OUTPUT_DIR)
        
        # Group files by their base ID
        image_pairs = {}
        total_size = 0
        
        for filename in files:
            if not filename.endswith('.jpg'):
                continue
            
            filepath = os.path.join(OUTPUT_DIR, filename)
            file_size = os.path.getsize(filepath)
            total_size += file_size
            
            # Extract base ID (everything before _original or _inky)
            if '_original.jpg' in filename:
                base_id = filename.replace('_original.jpg', '')
                if base_id not in image_pairs:
                    image_pairs[base_id] = {}
                image_pairs[base_id]['original'] = filename
            elif '_inky.jpg' in filename:
                base_id = filename.replace('_inky.jpg', '')
                if base_id not in image_pairs:
                    image_pairs[base_id] = {}
                image_pairs[base_id]['rotated'] = filename
        
        # Convert to list and add metadata
        images = []
        for base_id, pair in image_pairs.items():
            if 'original' in pair and 'rotated' in pair:
                # Extract timestamp from base_id
                timestamp_str = base_id.split('_')[0] + '_' + base_id.split('_')[1]
                try:
                    dt = datetime.strptime(timestamp_str, '%Y%m%d_%H%M%S')
                    timestamp = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = timestamp_str
                
                images.append({
                    'id': base_id,
                    'original': pair['original'],
                    'rotated': pair['rotated'],
                    'timestamp': timestamp
                })
        
        # Sort by timestamp (newest first)
        images.sort(key=lambda x: x['id'], reverse=True)
        
        return jsonify({
            'images': images,
            'total_pairs': len(images),
            'total_size': total_size
        })
        
    except Exception as e:
        print(f"Error loading gallery: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/cleanup', methods=['POST'])
def cleanup_images():
    """Delete all generated images"""
    try:
        if not os.path.exists(OUTPUT_DIR):
            return jsonify({'deleted_count': 0, 'freed_space': 0})
        
        files = os.listdir(OUTPUT_DIR)
        deleted_count = 0
        freed_space = 0
        
        for filename in files:
            if filename.endswith('.jpg'):
                filepath = os.path.join(OUTPUT_DIR, filename)
                file_size = os.path.getsize(filepath)
                os.remove(filepath)
                deleted_count += 1
                freed_space += file_size
        
        # Count pairs (2 files = 1 pair)
        pair_count = deleted_count // 2
        
        print(f"Cleanup: Deleted {deleted_count} files ({pair_count} pairs), freed {freed_space} bytes")
        
        return jsonify({
            'success': True,
            'deleted_count': pair_count,
            'deleted_files': deleted_count,
            'freed_space': freed_space
        })
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/delete/<image_id>', methods=['DELETE'])
def delete_image_pair(image_id):
    """Delete a specific image pair by ID"""
    try:
        if not os.path.exists(OUTPUT_DIR):
            return jsonify({'error': 'Output directory not found'}), 404
        
        # Find and delete both files for this image pair
        original_file = f"{image_id}_original.jpg"
        rotated_file = f"{image_id}_inky.jpg"
        
        deleted_files = []
        freed_space = 0
        
        for filename in [original_file, rotated_file]:
            filepath = os.path.join(OUTPUT_DIR, filename)
            if os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                os.remove(filepath)
                deleted_files.append(filename)
                freed_space += file_size
        
        if not deleted_files:
            return jsonify({'error': 'Image pair not found'}), 404
        
        print(f"Deleted image pair {image_id}: {deleted_files}, freed {freed_space} bytes")
        
        return jsonify({
            'success': True,
            'deleted_files': deleted_files,
            'freed_space': freed_space
        })
        
    except Exception as e:
        print(f"Error deleting image pair {image_id}: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/latest.jpg')
def get_latest_image():
    """Download the most recent inky (rotated) image as latest.jpg"""
    try:
        if not os.path.exists(OUTPUT_DIR):
            return "No images generated yet", 404
        
        # Get all inky files
        files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('_inky.jpg')]
        
        if not files:
            return "No images generated yet", 404
        
        # Sort by filename (which includes timestamp) to get most recent
        files.sort(reverse=True)
        latest_file = files[0]
        
        filepath = os.path.join(OUTPUT_DIR, latest_file)
        
        # Send file with filename 'latest.jpg'
        return send_file(
            filepath,
            mimetype='image/jpeg',
            as_attachment=True,
            download_name='latest.jpg'
        )
        
    except Exception as e:
        print(f"Error getting latest image: {str(e)}")
        return str(e), 500


if __name__ == '__main__':
    # Initialize model and DSPy once at startup
    print("\n🚀 Starting FLUX Image Generator for Inky Frame")
    
    # Initialize DSPy for prompt refinement
    init_dspy()
    
    # Initialize FLUX model
    init_model()
    
    # Run Flask app
    print("\n🌐 Starting Flask server on http://0.0.0.0:5000")
    print("Press Ctrl+C to stop\n")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
