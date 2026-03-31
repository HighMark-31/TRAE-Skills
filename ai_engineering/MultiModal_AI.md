# Skill: Multi-Modal AI

## Purpose
To work with AI models that can process and generate multiple types of content including text, images, audio, and video in a unified framework.

## When to Use
- When building applications that process images and text together
- When implementing vision-language tasks
- When generating images from text descriptions
- When analyzing visual content with natural language queries

## Procedure

### 1. Vision-Language Understanding
Process images with text queries using GPT-4 Vision.

```python
from openai import OpenAI
import base64

client = OpenAI()

def encode_image(image_path):
    """Encode image to base64."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, question):
    """Analyze image with text query."""
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content

# Example
analysis = analyze_image(
    "product.jpg",
    "What products are shown in this image? What are their key features?"
)
print(analysis)
```

### 2. Image Generation with DALL-E
Generate images from text descriptions.

```python
def generate_image(prompt, size="1024x1024", quality="standard"):
    """Generate image from text prompt."""
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size=size,
        quality=quality,
        n=1
    )
    
    image_url = response.data[0].url
    revised_prompt = response.data[0].revised_prompt
    
    return {
        "url": image_url,
        "revised_prompt": revised_prompt
    }

# Example
result = generate_image(
    "A futuristic smart home with voice-controlled devices and automated lighting",
    size="1024x1024"
)
print(f"Image URL: {result['url']}")
```

### 3. Image Editing and Variations
Modify and create variations of existing images.

```python
from PIL import Image
import io

def edit_image(original_image_path, mask_path, prompt):
    """Edit image with mask and prompt."""
    with open(original_image_path, "rb") as img_file:
        original_image = img_file.read()
    
    with open(mask_path, "rb") as mask_file:
        mask_image = mask_file.read()
    
    response = client.images.edit(
        model="dall-e-2",
        image=original_image,
        mask=mask_image,
        prompt=prompt,
        n=1,
        size="512x512"
    )
    
    return response.data[0].url

def create_variations(image_path):
    """Create variations of an image."""
    with open(image_path, "rb") as img_file:
        image_data = img_file.read()
    
    response = client.images.create_variation(
        image=image_data,
        n=3,
        size="1024x1024"
    )
    
    return [img.url for img in response.data]

# Example
edited_url = edit_image(
    "room.jpg",
    "room_mask.png",
    "Add a modern desk with computer setup"
)
print(f"Edited image: {edited_url}")
```

### 4. Multi-Modal Document Processing
Process documents with text and images.

```python
import pdf2image
import pytesseract

def process_multimodal_document(pdf_path):
    """Extract and analyze content from PDF with images."""
    # Convert PDF to images
    images = pdf2image.convert_from_path(pdf_path)
    
    results = []
    
    for i, image in enumerate(images):
        # Extract text using OCR
        text = pytesseract.image_to_string(image)
        
        # Encode image for GPT-4 Vision analysis
        import io
        import base64
        
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        base64_image = base64.b64encode(img_byte_arr).decode('utf-8')
        
        # Analyze image content
        vision_response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this document page. What type of content is shown?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                        }
                    ]
                }
            ]
        )
        
        results.append({
            "page": i + 1,
            "ocr_text": text,
            "visual_analysis": vision_response.choices[0].message.content
        })
    
    return results

# Example
document_results = process_multimodal_document("contract.pdf")
for page in document_results:
    print(f"Page {page['page']}: {page['visual_analysis']}")
```

### 5. Audio and Text Integration
Process audio with text analysis.

```python
import requests

def transcribe_and_analyze(audio_path):
    """Transcribe audio and analyze with text."""
    # Transcribe audio using Whisper
    with open(audio_path, "rb") as audio_file:
        transcription_response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text"
        )
    
    transcript = transcription_response
    
    # Analyze transcript with GPT-4
    analysis = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": f"Analyze this transcript for key topics, sentiment, and action items:\n\n{transcript}"
        }]
    )
    
    return {
        "transcript": transcript,
        "analysis": analysis.choices[0].message.content
    }

# Example
result = transcribe_and_analyze("meeting_recording.mp3")
print(f"Transcript: {result['transcript']}")
print(f"Analysis: {result['analysis']}")
```

### 6. Multi-Modal RAG System
Build RAG with image and text retrieval.

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class MultiModalRAG:
    def __init__(self):
        self.text_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.image_model = SentenceTransformer('clip-ViT-B-32')
        self.text_index = None
        self.image_index = None
        self.text_docs = []
        self.image_docs = []
    
    def add_text_documents(self, documents):
        """Add text documents to the index."""
        embeddings = self.text_model.encode(documents)
        
        if self.text_index is None:
            dimension = embeddings.shape[1]
            self.text_index = faiss.IndexFlatL2(dimension)
        
        self.text_index.add(embeddings.astype('float32'))
        self.text_docs.extend(documents)
    
    def add_image_documents(self, image_paths, descriptions):
        """Add images to the index."""
        embeddings = self.image_model.encode(image_paths)
        
        if self.image_index is None:
            dimension = embeddings.shape[1]
            self.image_index = faiss.IndexFlatL2(dimension)
        
        self.image_index.add(embeddings.astype('float32'))
        self.image_docs.extend(zip(image_paths, descriptions))
    
    def search(self, query, k=3):
        """Search across text and images."""
        # Search text
        if self.text_index:
            query_embedding = self.text_model.encode([query])
            text_distances, text_indices = self.text_index.search(
                query_embedding.astype('float32'), k
            )
            text_results = [
                (self.text_docs[i], text_distances[0][j])
                for j, i in enumerate(text_indices[0])
            ]
        else:
            text_results = []
        
        # Search images
        if self.image_index:
            query_embedding = self.image_model.encode([query])
            image_distances, image_indices = self.image_index.search(
                query_embedding.astype('float32'), k
            )
            image_results = [
                (self.image_docs[i], image_distances[0][j])
                for j, i in enumerate(image_indices[0])
            ]
        else:
            image_results = []
        
        return {
            "text_results": text_results,
            "image_results": image_results
        }

# Example usage
rag = MultiModalRAG()

rag.add_text_documents([
    "Python is a high-level programming language",
    "JavaScript is used for web development"
])

rag.add_image_documents(
    ["python_logo.png", "js_logo.png"],
    ["Python programming language logo", "JavaScript logo"]
)

results = rag.search("programming languages")
print(results)
```

## Constraints
- **Image Size**: Vision models have limits on image dimensions and file sizes
- **Cost**: Vision and image generation APIs are more expensive than text-only
- **Quality**: Generated images may not always match expectations
- **Processing Time**: Image processing is slower than text-only operations
- **Accuracy**: OCR accuracy varies based on image quality
- **Privacy**: Be careful with sensitive visual content

## Expected Output
Comprehensive multi-modal AI applications that can seamlessly process and generate text, images, and audio content with high accuracy and integration.
