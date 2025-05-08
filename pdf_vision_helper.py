import os
import base64
from openai import OpenAI

client = OpenAI()

def extract_text_with_gpt4v(pdf_page_image):
    """
    Use GPT-4 Vision to extract text from a PDF page image
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OpenAI API key not found. Please set the OPENAI_API_KEY environment variable."  

    client = OpenAI(api_key=api_key)
        
        # Convert the image to base64
        image_base64 = base64.b64encode(pdf_page_image).decode('utf-8')
        
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please extract all the text from this image, preserving paragraphs and layout. Format the text as a JSON object with 'paragraphs' as an array of text blocks."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096
        )
        
        return response.choices[0].message.content
    except Exception as e:
        return f"Error in GPT-4V text extraction: {str(e)}"
