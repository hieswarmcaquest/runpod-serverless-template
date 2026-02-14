import gradio as gr
from sample_request import convert_text_to_speech_using_api


with gr.Blocks(title="Kokoro TTS (Local Docker)") as demo:
    gr.Markdown("# 🦜 Kokoro TTS - Local CPU Docker")

    with gr.Row():
        with gr.Column():
            text_input = gr.Textbox(
                label="Input Text", lines=3, placeholder="Type something here..."
            )
            with gr.Row():
                voice_dropdown = gr.Dropdown(
                    choices=[   
                        "af_heart",
                        "af_alloy",
                        "af_aoede",
                        "af_bella",
                        "af_jessica",
                        "af_kore",
                        "af_nicole",
                        "af_nova",
                        "af_river",
                        "af_sarah",
                        "af_sky",
                        "am_adam",
                        "am_echo",
                        "am_eric",
                        "am_fenrir",
                        "am_liam",
                        "am_michael",
                        "am_onyx",
                        "am_puck",
                        "am_santa",
                        "bf_alice",
                        "bf_emma",
                        "bf_isabella",
                        "bf_lily",
                        "bm_daniel",
                        "bm_fable",
                        "bm_george",
                        "bm_lewis",
                    ],
                    value="af_heart",
                    label="Voice",
                )
                speed_slider = gr.Slider(0.5, 2.0, value=1.0, step=0.1, label="Speed")

            submit_btn = gr.Button("Generate Audio", variant="primary")

        with gr.Column():
            audio_output = gr.Audio(label="Output Audio", type="numpy")

    # Connect the UI elements to the function
    # Note: Gradio expects the function to return (sample_rate, numpy_array) for audio
    submit_btn.click(
        fn=convert_text_to_speech_using_api,
        inputs=[text_input, voice_dropdown, speed_slider],
        outputs=[audio_output],
        api_name="generate_speech"
    )

if __name__ == "__main__":
    demo.launch()
