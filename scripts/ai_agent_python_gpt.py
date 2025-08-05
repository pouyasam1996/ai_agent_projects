import openai
import base64
import io
from PIL import Image
import sys
import os

API_KEY = ''

def process_screenshot(screenshot_path):
    """Process screenshot and get AI analysis for Python output"""
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

    # Prompt for Python code output
    prompt = """
    Analyze the screenshot carefully and provide a well-structured response.

    First, identify what type of content this is:
    - Coding problem (algorithm, data structure, debugging, etc.)
    - General question or text
    - Nothing significant to analyze

    If it's a coding problem, provide:
    1. PROBLEM ANALYSIS
    Brief description of what the problem is asking for.

    2. SOLUTION DESCRIPTION (Common Approach)
    Provide an overview of the approach of solving the problem in top level and why it's a common approach.

    3. SOLUTION 1 (Common Approach)
    Provide clean, well-commented Python code with proper indentation.

    4. SOLUTION DESCRIPTION (Alternative Approach)
    Provide an overview of the approach of solving the problem in top level and why it's a alternative approach. 

    5. SOLUTION 2 (Alternative Approach)
    Provide a different Python approach with clean code.

    6. EXPLANATIONS
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

    Format your response in a LaTeX format for easy display.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
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

        result = response.choices[0].message.content
        # Save result to file - FIXED: Use relative path that works from project root
        results_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results.txt")
        with open(results_path, "w") as f:
            f.write(result)
        return result

    except Exception as e:
        return f"AI processing error: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide screenshot path as argument")
        sys.exit(1)
    screenshot_path = sys.argv[1]
    result = process_screenshot(screenshot_path)
    print("AI Result:", result)