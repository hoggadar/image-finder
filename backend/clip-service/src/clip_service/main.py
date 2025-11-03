from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel
import io
import uvicorn


app = FastAPI(title="CLIP Similarity API", version="1.0.0")

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
model.eval()
print("Model loaded successfully!")


@app.post("/similarity")
async def calculate_similarity(
    image: UploadFile = File(..., description="Image for analysis"),
    text: str = Form(..., description="Text description for comparison")
):
    try:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        image_inputs = processor(images=pil_image, return_tensors="pt")
        text_inputs = processor(text=[text], return_tensors="pt", padding=True)
        
        with torch.no_grad():
            image_embeds = model.get_image_features(**image_inputs)
            image_embeds = image_embeds / image_embeds.norm(p=2, dim=-1, keepdim=True)
            
            text_embeds = model.get_text_features(**text_inputs)
            text_embeds = text_embeds / text_embeds.norm(p=2, dim=-1, keepdim=True)
        
        similarity = (text_embeds @ image_embeds.T).item()
        probability = (similarity + 1) / 2
        
        if similarity > 0.8:
            interpretation = "Very high match"
        elif similarity > 0.6:
            interpretation = "High match"
        elif similarity > 0.4:
            interpretation = "Medium match"
        elif similarity > 0.2:
            interpretation = "Low match"
        else:
            interpretation = "Very low match"
        
        return {
            "success": True,
            "similarity": round(similarity, 4),
            "probability": round(probability, 4),
            "interpretation": interpretation,
            "details": {
                "text": text,
                "image_shape": pil_image.size,
                "embedding_dim": image_embeds.shape[-1]
            }
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@app.get("/health")
async def health():
    return {"status": "healthy", "model": "openai/clip-vit-base-patch32"}


if __name__ == "__main__":  
    uvicorn.run(app)