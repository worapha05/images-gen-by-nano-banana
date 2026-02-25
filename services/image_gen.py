import io
import random
from google import genai
from google.genai import types
from PIL import Image
from fastapi import UploadFile
from io import BytesIO
from typing import List
import base64

class ImageGenServiceError(Exception):
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code

class ImageGenService:
    SAFETY_SYSTEM_PROMPT = (
        "You are an educational image generator.",
        "You MUST ONLY generate images that are safe, appropriate, and suitable for an educational platform used by students of all ages.",
        "STRICTLY PROHIBITED content: violence, blood, gore, weapons, fighting, nudity, sexual content, drugs, alcohol, hate speech, horror, self-harm, gambling, or any content inappropriate for a school environment.",
        "If the user's request conflicts with these rules, generate a safe educational alternative instead.",
        "Always prioritize child-safe, educational, and positive imagery."
    )

    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)

    def generate_image(self,
        files_bytes: list[bytes] | None = None, 
        prompt: str | None = None,
        aspect_ratio: str = "1:1",
        resolution: str = "1K"
        ) -> dict:
        
        if prompt and prompt.strip():
            prompt = self.SAFETY_SYSTEM_PROMPT + (prompt.strip(), )
        else:
            prompt = self.SAFETY_SYSTEM_PROMPT

        contents = [prompt]

        aspect_ratio_arr = ["1:1","2:3","3:2","3:4","4:3","4:5","5:4","9:16","16:9","21:9"]
        resolution_arr = ["1K", "2K", "4K"]

        if aspect_ratio not in aspect_ratio_arr:
            aspect_ratio = "1:1"
        
        if resolution not in resolution_arr:
            resolution = "1K"
        
        try:
            if files_bytes:
                images = []

                for file_byte in files_bytes:
                    img = Image.open(BytesIO(file_byte))
                    images.append(img)

                contents.extend(images)

        except Exception as e:
            raise ImageGenServiceError(
                message="ImageGenService Error Can not process Image bytes",
                code="IMAGE_PROCESSING_ERROR"
            )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=contents,
                config=types.GenerateContentConfig(
                    image_config=types.ImageConfig(
                        aspect_ratio=aspect_ratio,
                        image_size=resolution
                    ),
                )
            )

            image = None

            if response.parts:
                for part in response.parts:
                    if part.inline_data is not None:
                        image = part.inline_data.data

            if image:
                image = Image.open(io.BytesIO(image))
                image_buffer = io.BytesIO()
                image.save(image_buffer, format="PNG")
                image_base64 = base64.b64encode(image_buffer.getvalue()).decode("utf-8")

                return {
                    "image": f"data:image/png;base64,{image_base64}",
                    "size": image.size
                }
            
            else:
                raise ImageGenServiceError(
                    message="Model returned no image (blocked or empty response).",
                    code="NO_IMAGE_RETURNED"
                )
        except Exception as e:
            raise ImageGenServiceError(
                message=f"Model returned no image (blocked or empty response).",
                code="NO_IMAGE_RETURNED"
            )

    async def convert_files_to_bytes(self, files: List[UploadFile]) -> List[bytes]:
        try:
            files_bytes: List[bytes] = []

            for file in files:
                file_content = await file.read()
                files_bytes.append(file_content)

            return files_bytes
        except Exception as e:
            raise ImageGenServiceError(
                message="ImageGenService Error Can not convert uploaded images to bytes",
                code="IMAGE_CONVERSION_ERROR"
            )
    
    def create_prompt(self, prompt: str | None, files: list[str] | None) -> str:
            if files:  
                image_count = len(files)
                if prompt and prompt.strip():
                    if image_count == 1:
                        final_prompt = f"[EDUCATION-SAFE ONLY] Using the uploaded image as reference, create an educational illustration: {prompt.strip()} Include educational elements like classrooms, books, students, teachers, learning materials, or academic settings while maintaining the visual style of the reference image. Do NOT include any violence, weapons, blood, nudity, or inappropriate content."
                    else:
                        final_prompt = f"[EDUCATION-SAFE ONLY] Using the {image_count} uploaded images as references, create an educational illustration: {prompt.strip()} Combine visual styles from all images and integrate educational themes like learning environments, educational materials, students, teachers, and academic activities. Do NOT include any violence, weapons, blood, nudity, or inappropriate content."
                
                else:
                    if image_count == 1:
                        final_prompt = "[EDUCATION-SAFE ONLY] Transform this image into an educational context. Add educational elements like books, students, teachers, desks, whiteboards, learning materials, or classroom settings while maintaining the original style and composition. Do NOT include any violence, weapons, blood, nudity, or inappropriate content."
                    else:
                        final_prompt = f"[EDUCATION-SAFE ONLY] Using these {image_count} images as inspiration, create an educational illustration that combines elements from all references. Include learning environments, educational materials, students engaged in learning activities, and academic settings. Do NOT include any violence, weapons, blood, nudity, or inappropriate content."
            
            else:  
                if prompt and prompt.strip():
                    final_prompt = f"[EDUCATION-SAFE ONLY] Create an educational illustration: {prompt.strip()} Include learning environments (classroom, library, lab), educational materials (books, computers, supplies), and students or teachers in learning activities. Do NOT include any violence, weapons, blood, nudity, or inappropriate content."
                else:
                    default_prompts = [
                        "Create a modern classroom with diverse students learning together, educational posters on walls, books on shelves, and a teacher facilitating discussion. Bright and inspiring atmosphere.",
                        
                        "Generate a student's study desk with open textbooks, notebooks, laptop, pens, desk lamp, and coffee mug. Include motivational elements and organized learning materials.",
                        
                        "Create an educational concept showing books transforming into a tree of knowledge with different subjects as branches (science, math, art, language). Students exploring and light bulbs representing ideas.",
                        
                        "Design a learning space with reading corner, group study area, computers, and presentation zone. Show diverse students learning in different ways with educational displays.",
                        
                        "Generate a beautiful library with bookshelves, reading nooks, study tables with focused students, natural lighting, and peaceful learning atmosphere.",
                        
                        "Create a science lab with students conducting experiments, microscopes, safety equipment, colorful chemicals, educational posters, and teacher guiding discovery learning.",
                        
                        "Design an art classroom with students creating artwork, easels, art supplies, displayed student work, and instructor demonstrating techniques. Creative and inspiring environment.",
                        
                        "Generate an outdoor education scene with students and teachers in nature, observing plants and insects, taking notes, using magnifying glasses, and learning about ecosystems."
                    ]
                    final_prompt = random.choice(default_prompts)

            return final_prompt
    
    def is_valid_image_type(self, content_type: str) -> bool:
        if not content_type:
            return False
        
        allowed = ["image/jpeg", "image/png"]
        return any(allowed_type in content_type for allowed_type in allowed)