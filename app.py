import os
from dotenv import load_dotenv, find_dotenv
import gradio as gr

import msuliot.openai_helper as oai  # Ensure this helper handles OpenAI Chat API interactions

from env_config import envs

# Load environment variables
env = envs()
load_dotenv(find_dotenv())

# Main function to handle code generation
def main(query):
    print("Start: Main function")

    # Initialize OpenAI chat model
    oaic = oai.openai_chat(env.openai_key, model="gpt-4")  # Use GPT-4 or any preferred model

    # Prepare the system prompt for the LLM
    system_prompt_full = f"""
    You are an honest, professional, and positive AI assistant specialized in code generation. 
    Your task is to generate high-quality, enterprise-level code based on user queries. 
    If the user's query is related to code generation, provide an appropriate code response. 
    If the query is not related to code generation, respond with: "Please provide a query related to code generation."
    """

    oaic.add_message("system", system_prompt_full)
    oaic.add_message("user", query)

    # Get the response from OpenAI
    try:
        response = oaic.execute()
        final_output = response
    except Exception as e:
        final_output = f"⚠️ An error occurred while generating the code: {str(e)}"

    return final_output

############## Gradio UI ################

gr.close_all()  # This line ensures that any previously running Gradio interfaces are closed before launching a new one.

with gr.Blocks() as demo:
    gr.Markdown("# Blades of Grass - AI Code Generator")
    gr.Markdown("""
    Blades of Grass is an AI Assistant that leverages OpenAI to generate high-quality, enterprise-level code snippets based on your queries.
    """)

    with gr.Row():
        with gr.Column():
            user_prompt = gr.Textbox(
                label="Your Code Query",
                lines=8,
                placeholder="e.g., Create a Python function to sort a list of numbers."
            )
            submit_btn = gr.Button("Generate Code")

        response = gr.Markdown(label="Generated Code", value="")  # It shows in the same row with column component's
    
    submit_btn.click(
        fn=main,
        inputs=user_prompt,
        outputs=response  # Only the response for the generated code is returned now
    )

demo.launch(server_name="localhost", server_port=8765)