#!/usr/bin/env python3
"""
Test script to verify FLUX model installation and image generation
"""

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image

def test_installation():
    """Test if all dependencies are installed"""
    print("Testing installation...")
    
    try:
        import flask
        print("✓ Flask installed")
    except ImportError:
        print("✗ Flask not installed - run: pip install flask")
        return False
    
    try:
        import torch
        print(f"✓ PyTorch installed - Version: {torch.__version__}")
        print(f"  CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"  CUDA device: {torch.cuda.get_device_name(0)}")
    except ImportError:
        print("✗ PyTorch not installed")
        return False
    
    try:
        import diffusers
        print(f"✓ Diffusers installed - Version: {diffusers.__version__}")
    except ImportError:
        print("✗ Diffusers not installed")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow installed")
    except ImportError:
        print("✗ Pillow not installed")
        return False
    
    return True


def test_model_loading():
    """Test loading the FLUX model"""
    print("\nTesting model loading...")
    print("(This will download ~8GB on first run)")
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        
        print(f"Loading model on {device}...")
        pipe = Flux2KleinPipeline.from_pretrained(
            "black-forest-labs/FLUX.2-klein-4B",
            torch_dtype=dtype
        )
        
        if device == "cuda":
            pipe.enable_model_cpu_offload()
        
        print("✓ Model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return False


def test_image_generation():
    """Test generating a simple image"""
    print("\nTesting image generation...")
    
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        
        pipe = Flux2KleinPipeline.from_pretrained(
            "black-forest-labs/FLUX.2-klein-4B",
            torch_dtype=dtype
        )
        
        if device == "cuda":
            pipe.enable_model_cpu_offload()
        
        print("Generating test image...")
        image = pipe(
            "A simple red circle on white background",
            height=800,
            width=480,
            guidance_scale=1.0,
            num_inference_steps=4,
            generator=torch.Generator(device=device).manual_seed(42)
        ).images[0]
        
        # Rotate and save
        rotated = image.rotate(90, expand=True)
        if rotated.mode != 'RGB':
            rotated = rotated.convert('RGB')
        
        rotated.save("test_output.jpg", "JPEG", quality=70)
        print(f"✓ Image generated and saved as test_output.jpg")
        print(f"  Size: {rotated.size}")
        return True
        
    except Exception as e:
        print(f"✗ Failed to generate image: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("FLUX Image Generator - Installation Test")
    print("=" * 60)
    
    if not test_installation():
        print("\n❌ Installation test failed!")
        print("Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        exit(1)
    
    print("\n" + "=" * 60)
    user_input = input("Proceed with model loading test? (y/n): ")
    
    if user_input.lower() == 'y':
        if test_model_loading():
            print("\n" + "=" * 60)
            user_input = input("Proceed with image generation test? (y/n): ")
            
            if user_input.lower() == 'y':
                if test_image_generation():
                    print("\n✅ All tests passed!")
                    print("You can now run the Flask app with: python app.py")
                else:
                    print("\n❌ Image generation test failed!")
        else:
            print("\n❌ Model loading test failed!")
    
    print("\n" + "=" * 60)
