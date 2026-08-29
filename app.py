        # ---- Show Shed Map ----
        first_bin = result[BIN_COL].iloc[0]
        shed = get_shed(first_bin)

        if shed:
            st.markdown(f"### 📍 This part is located in **Shed {shed}**")

            pdf_file = f"Shed {shed}.pdf"

            try:
                # Download button
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()
                    st.download_button(
                        label=f"📄 Download Shed {shed} Map (PDF)",
                        data=pdf_bytes,
                        file_name=pdf_file,
                        mime="application/pdf"
                    )

                # Display PDF using base64 (works on Streamlit Cloud)
                import base64
                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                pdf_display = f'''
                    <iframe 
                        src="data:application/pdf;base64,{base64_pdf}" 
                        width="100%" 
                        height="650" 
                        type="application/pdf">
                    </iframe>
                '''
                st.markdown(pdf_display, unsafe_allow_html=True)

            except FileNotFoundError:
                st.warning(f"Map file **{pdf_file}** not found. Please make sure it is uploaded to the GitHub repository.")
        else:
            st.info("Could not automatically detect the shed for this bin.")
