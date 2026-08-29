        # Show Shed Map
        first_bin = result[BIN_COL].iloc[0]
        shed = get_shed(first_bin)

        if shed:
            st.markdown(f"### 📍 This part is located in **Shed {shed}**")

            pdf_file = f"Shed {shed}.pdf"

            try:
                with open(pdf_file, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    label=f"📄 Download / View Shed {shed} Map (PDF)",
                    data=pdf_bytes,
                    file_name=pdf_file,
                    mime="application/pdf",
                    type="primary"
                )

                st.info("Click the button above to open or download the shed map.")

            except FileNotFoundError:
                st.warning(f"Map file **{pdf_file}** not found. Please upload it to the GitHub repository.")
        else:
            st.info("Could not automatically detect the shed for this bin.")
