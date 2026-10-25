import sys
from fpdf import FPDF

# Define a custom class that inherits from FPDF to customize page components
class Shirtificate(FPDF):
    # Overriding the header method automatically sets the document banner on every new page
    def header(self):
        # Configure a bold Helvetica font with a size of 45 points
        self.set_font("Helvetica", "B", 45)
        # Create a full-width text cell centered horizontally to display the title
        # new_x and new_y arguments define where the layout cursor moves next
        self.cell(0, 40, "CS50 Shirtificate", align="C", new_x="LMARGIN", new_y="NEXT")
        # Add a vertical line break gap spacing of 10 units (millimeters)
        self.ln(10)

    # Custom method to overlay the personalized name text cleanly over the shirt image
    def text_on_shirt(self, name):
        # Configure a smaller, bold Helvetica font style for the shirt message text
        self.set_font("Helvetica", "B", 24)
        # Change the active text color properties to pure white RGB (255, 255, 255)
        self.set_text_color(255, 255, 255)

        # Reposition the document's rendering vertical track position directly to 140 mm
        self.set_y(140)
        # Print the personalized text centered within the bounding region
        self.cell(0, 10, f"{name} took CS50", align="C")

def main():
    # Prompt the user for a name string and remove outside padding whitespaces
    name = input("Name: ").strip()
    # Guard clause: stop the script execution immediately if no text was provided
    if not name:
        sys.exit("Name cannot be empty")

    # Instantiate the custom PDF renderer class configured for Portrait mode and standard A4 sizes
    pdf = Shirtificate(orientation="P", unit="mm", format="A4")

    # Disable automatic page breaks to prevent elements from jumping onto an accidental second sheet
    pdf.set_auto_page_break(auto=False)

    # Initialize a blank sheet page area to map the graphic shapes
    pdf.add_page()

    # Define sizing variables for positioning the graphic asset matching standard layout metrics
    shirt_width = 180
    # Calculate the exact center horizontal coordinate (A4 width is 210mm)
    shirt_x = (210 - shirt_width) / 2
    shirt_y = 80

    try:
        # Load and render the external shirt graphic file template onto the page workspace coordinates
        pdf.image("shirtificate.png", x=shirt_x, y=shirt_y, w=shirt_width)
    # Handle environment exceptions cleanly if the source background image asset file is missing
    except FileNotFoundError:
        sys.exit("Error: 'shirtificate.png' not found in the current directory.")

    # Execute our custom text placement logic method to render the user text onto the shirt area
    pdf.text_on_shirt(name)

    # Compile the complete document layout instructions structure and save it to disk
    pdf.output("shirtificate.pdf")

if __name__ == "__main__":
    main()
