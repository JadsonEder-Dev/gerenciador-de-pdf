import os
from tkinter import Tk, Button, filedialog, Label
from tkinterdnd2 import DND_FILES, TkinterDnD
from pypdf import PdfReader, PdfWriter

class PDFProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de PDFs com Drag and Drop")
        self.first_file = None
        self.second_file = None

        # Labels de instrução
        self.label = Label(root, text="Arraste os arquivos ou clique nos botões abaixo", wraplength=300)
        self.label.pack(pady=10)

        # Botões de seleção
        self.btn_select_first = Button(root, text="Selecionar Primeiro PDF", command=self.select_first_file)
        self.btn_select_first.pack(pady=5)

        self.label_first_file = Label(root, text="Nenhum arquivo selecionado")
        self.label_first_file.pack(pady=5)

        self.btn_select_second = Button(root, text="Selecionar Segundo PDF", command=self.select_second_file)
        self.btn_select_second.pack(pady=5)

        self.label_second_file = Label(root, text="Nenhum arquivo selecionado")
        self.label_second_file.pack(pady=5)

        # Botão para processar os PDFs
        self.btn_process = Button(root, text="Processar PDFs", command=self.process_pdfs, state="disabled")
        self.btn_process.pack(pady=20)

        # Mensagem de status
        self.label_status = Label(root, text="")
        self.label_status.pack()

        # Configurar Drag and Drop
        self.setup_drag_and_drop()

    def setup_drag_and_drop(self):
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.handle_drop)

    def handle_drop(self, event):
        file_path = os.path.normpath(event.data.strip("{}"))
        if not self.first_file:
            self.first_file = file_path
            self.label_first_file.config(text=f"Primeiro arquivo: {os.path.basename(file_path)}")
        elif not self.second_file:
            self.second_file = file_path
            self.label_second_file.config(text=f"Segundo arquivo: {os.path.basename(file_path)}")
        self.update_process_button_state()

    def select_first_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.first_file = os.path.normpath(file_path)
            self.label_first_file.config(text=f"Primeiro arquivo: {os.path.basename(file_path)}")
        self.update_process_button_state()

    def select_second_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if file_path:
            self.second_file = os.path.normpath(file_path)
            self.label_second_file.config(text=f"Segundo arquivo: {os.path.basename(file_path)}")
        self.update_process_button_state()

    def update_process_button_state(self):
        if self.first_file and self.second_file:
            self.btn_process.config(state="normal")
        else:
            self.btn_process.config(state="disabled")

    def process_pdfs(self):
        try:
            modified_pdf_writer = self.remove_pages(self.first_file, pages_to_keep=range(4))
            merged_pdf_writer = self.merge_pdfs(modified_pdf_writer, self.second_file)
            self.save_pdf(merged_pdf_writer)

            self.label_status.config(text="PDFs processados e salvos com sucesso!")
        except Exception as e:
            self.label_status.config(text=f"Erro ao processar PDFs: {e}")

    def remove_pages(self, input_pdf, pages_to_keep):
        reader = PdfReader(input_pdf)
        writer = PdfWriter()

        for page_number in pages_to_keep:
            if page_number < len(reader.pages):
                writer.add_page(reader.pages[page_number])

        return writer

    def merge_pdfs(self, pdf_writer, other_pdf):
        reader = PdfReader(other_pdf)
        for page in reader.pages:
            pdf_writer.add_page(page)

        return pdf_writer

    def save_pdf(self, pdf_writer):
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
        )
        if output_path:
            with open(output_path, "wb") as f:
                pdf_writer.write(f)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = PDFProcessorApp(root)
    root.mainloop()
