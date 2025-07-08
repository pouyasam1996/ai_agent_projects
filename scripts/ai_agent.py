import openai
import base64
import io
from PIL import Image

API_KEY = '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'


def process_screenshot(screenshot_path):
    """Process screenshot and get AI analysis"""
    # Initialize OpenAI client
    client = openai.OpenAI(api_key=API_KEY)

    # Resize and encode image
    try:
        with Image.open(screenshot_path) as img:
            img.thumbnail((512, 512))  # Resize to max 512x512
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
            print(f"Encoded image size: {len(encoded_image)} bytes")
    except Exception as e:
        return f"Image processing error: {e}"

    # Enhanced prompt for better structured output
    prompt = """
    Analyze the screenshot carefully and provide a well-structured response.

    First, identify what type of content this is:
    - Coding problem (algorithm, data structure, debugging, etc.)
    - General question or text
    - Nothing significant to analyze

    If it's a coding problem, provide:
    1. PROBLEM ANALYSIS
    Brief description of what the problem is asking for.

    2. SOLUTION 1 (Common Approach)
    Provide clean, well-commented code with proper indentation.
    Include the programming language used.

    3. SOLUTION 2 (Alternative Approach)
    Provide a different approach with clean code.
    Include the programming language used.

    4. EXPLANATIONS
    Explain how each solution works and why you chose these approaches.
    Include time and space complexity if applicable.

    If it's a general question, provide:
    1. QUESTION SUMMARY
    What is being asked?

    2. DETAILED ANSWER
    Comprehensive response to the question.

    3. KEY POINTS
    Important takeaways or considerations.

    If there's nothing significant to analyze, simply respond:
    "No problem or question detected in the screenshot."

    Format your response in a latex format so I can show it easily.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                        }
                    ]
                }
            ],
            temperature=0.2,
            max_tokens=2000
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI processing error: {e}"