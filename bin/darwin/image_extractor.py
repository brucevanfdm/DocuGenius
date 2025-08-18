# -*- coding: utf-8 -*-
"""
DocuGenius Image Extraction Module
Extracts images from PDF, DOCX, and PPTX files and organizes them in structured folders.
"""

import sys
import os
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Tuple, Optional

class ImageExtractor:
    """Main class for extracting images from documents"""
    
    def __init__(self, document_path: str, output_dir: str = None):
        self.document_path = Path(document_path)
        self.document_name = self.document_path.stem
        self.document_ext = self.document_path.suffix.lower()
        
        # Set output directory - use images/{document_name}/ structure
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            # Default to images folder in same directory as document
            self.output_dir = self.document_path.parent / "images" / self.document_name
        
        self.extracted_images = []
        self.image_counter = 1
        
    def extract_images(self) -> Dict:
        """Extract images from document and return metadata"""
        try:
            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)
            
            if self.document_ext == '.pdf':
                return self._extract_from_pdf()
            elif self.document_ext == '.docx':
                return self._extract_from_docx()
            elif self.document_ext == '.pptx':
                return self._extract_from_pptx()
            else:
                return {
                    'success': False,
                    'error': f'Unsupported document type: {self.document_ext}',
                    'images': []
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting images: {str(e)}',
                'images': []
            }
    
    def _extract_from_pdf(self) -> Dict:
        """Extract images from PDF using PyMuPDF (fitz)"""
        try:
            import fitz  # PyMuPDF
        except ImportError:
            try:
                # Fallback to pdfplumber for basic image detection
                import pdfplumber
                return self._extract_from_pdf_pdfplumber()
            except ImportError:
                return {
                    'success': False,
                    'error': 'PDF image extraction requires PyMuPDF (pip install PyMuPDF) or pdfplumber',
                    'images': []
                }
        
        try:
            doc = fitz.open(str(self.document_path))
            images_extracted = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                image_list = page.get_images()
                
                for img_index, img in enumerate(image_list):
                    # Get image data
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    
                    # Skip if image is too small (likely decorative)
                    if pix.width < 50 or pix.height < 50:
                        pix = None
                        continue
                    
                    # Determine image format and extension
                    if pix.n - pix.alpha < 4:  # GRAY or RGB
                        img_ext = "png"
                        img_data = pix.tobytes("png")
                    else:  # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        img_ext = "png"
                        img_data = pix1.tobytes("png")
                        pix1 = None
                    
                    # Generate unique filename
                    img_filename = self._generate_image_filename(
                        f"page_{page_num + 1}_img_{img_index + 1}", 
                        img_ext
                    )
                    img_path = self.output_dir / img_filename
                    
                    # Save image
                    with open(img_path, "wb") as img_file:
                        img_file.write(img_data)
                    
                    # Add to extracted images list
                    image_info = {
                        'filename': img_filename,
                        'path': str(img_path),
                        'relative_path': f"images/{self.document_name}/{img_filename}",
                        'page': page_num + 1,
                        'width': pix.width,
                        'height': pix.height,
                        'format': img_ext.upper(),
                        'size_bytes': len(img_data)
                    }
                    images_extracted.append(image_info)
                    self.extracted_images.append(image_info)
                    
                    pix = None
            
            doc.close()
            
            return {
                'success': True,
                'document': str(self.document_path),
                'output_dir': str(self.output_dir),
                'images_count': len(images_extracted),
                'images': images_extracted
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting images from PDF: {str(e)}',
                'images': []
            }
    
    def _extract_from_pdf_pdfplumber(self) -> Dict:
        """Fallback PDF image extraction using pdfplumber (limited functionality)"""
        try:
            import pdfplumber
            
            # pdfplumber doesn't directly extract images, but we can detect them
            # This is a basic implementation that creates placeholder entries
            with pdfplumber.open(str(self.document_path)) as pdf:
                images_detected = []
                
                for page_num, page in enumerate(pdf.pages):
                    # Check if page has images (basic detection)
                    if hasattr(page, 'images') and page.images:
                        for img_index, img_obj in enumerate(page.images):
                            # Create placeholder entry since we can't extract actual image data
                            image_info = {
                                'filename': f"page_{page_num + 1}_img_{img_index + 1}_placeholder.txt",
                                'path': str(self.output_dir / f"page_{page_num + 1}_img_{img_index + 1}_placeholder.txt"),
                                'relative_path': f"images/{self.document_name}/page_{page_num + 1}_img_{img_index + 1}_placeholder.txt",
                                'page': page_num + 1,
                                'width': img_obj.get('width', 0),
                                'height': img_obj.get('height', 0),
                                'format': 'PLACEHOLDER',
                                'size_bytes': 0,
                                'note': 'Image detected but not extracted (requires PyMuPDF for full extraction)'
                            }
                            images_detected.append(image_info)
                            
                            # Create placeholder file
                            placeholder_path = self.output_dir / image_info['filename']
                            with open(placeholder_path, 'w') as f:
                                f.write(f"Image placeholder for page {page_num + 1}, image {img_index + 1}\n")
                                f.write("Install PyMuPDF (pip install PyMuPDF) for actual image extraction.\n")
                
                return {
                    'success': True,
                    'document': str(self.document_path),
                    'output_dir': str(self.output_dir),
                    'images_count': len(images_detected),
                    'images': images_detected,
                    'note': 'Limited extraction - install PyMuPDF for full image extraction'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Error with pdfplumber fallback: {str(e)}',
                'images': []
            }

    def _extract_from_docx(self) -> Dict:
        """Extract images from DOCX files"""
        try:
            import docx
            from docx.document import Document
            from docx.oxml.table import CT_Tbl
            from docx.oxml.text.paragraph import CT_P
            from docx.table import _Cell, Table
            from docx.text.paragraph import Paragraph
        except ImportError:
            return {
                'success': False,
                'error': 'DOCX image extraction requires python-docx (pip install python-docx)',
                'images': []
            }

        try:
            doc = docx.Document(str(self.document_path))
            images_extracted = []

            # Extract images from document relationships
            for rel in doc.part.rels.values():
                if "image" in rel.target_ref:
                    # Get image data
                    image_part = rel.target_part
                    image_data = image_part.blob

                    # Determine file extension from content type
                    content_type = image_part.content_type
                    if 'jpeg' in content_type or 'jpg' in content_type:
                        img_ext = 'jpg'
                    elif 'png' in content_type:
                        img_ext = 'png'
                    elif 'gif' in content_type:
                        img_ext = 'gif'
                    elif 'bmp' in content_type:
                        img_ext = 'bmp'
                    else:
                        img_ext = 'png'  # Default fallback

                    # Generate unique filename
                    img_filename = self._generate_image_filename(
                        f"docx_img_{len(images_extracted) + 1}",
                        img_ext
                    )
                    img_path = self.output_dir / img_filename

                    # Save image
                    with open(img_path, "wb") as img_file:
                        img_file.write(image_data)

                    # Add to extracted images list
                    image_info = {
                        'filename': img_filename,
                        'path': str(img_path),
                        'relative_path': f"images/{self.document_name}/{img_filename}",
                        'format': img_ext.upper(),
                        'size_bytes': len(image_data),
                        'source': 'docx_relationship'
                    }
                    images_extracted.append(image_info)
                    self.extracted_images.append(image_info)

            return {
                'success': True,
                'document': str(self.document_path),
                'output_dir': str(self.output_dir),
                'images_count': len(images_extracted),
                'images': images_extracted
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting images from DOCX: {str(e)}',
                'images': []
            }

    def _extract_from_pptx(self) -> Dict:
        """Extract images from PPTX files"""
        try:
            import pptx
            from pptx import Presentation
        except ImportError:
            return {
                'success': False,
                'error': 'PPTX image extraction requires python-pptx (pip install python-pptx)',
                'images': []
            }

        try:
            prs = Presentation(str(self.document_path))
            images_extracted = []

            for slide_num, slide in enumerate(prs.slides):
                for shape in slide.shapes:
                    if hasattr(shape, 'image'):
                        # Get image data
                        image = shape.image
                        image_data = image.blob

                        # Determine file extension from content type
                        content_type = image.content_type
                        if 'jpeg' in content_type or 'jpg' in content_type:
                            img_ext = 'jpg'
                        elif 'png' in content_type:
                            img_ext = 'png'
                        elif 'gif' in content_type:
                            img_ext = 'gif'
                        elif 'bmp' in content_type:
                            img_ext = 'bmp'
                        else:
                            img_ext = 'png'  # Default fallback

                        # Generate unique filename
                        img_filename = self._generate_image_filename(
                            f"slide_{slide_num + 1}_img_{len([s for s in slide.shapes if hasattr(s, 'image')]) + 1}",
                            img_ext
                        )
                        img_path = self.output_dir / img_filename

                        # Save image
                        with open(img_path, "wb") as img_file:
                            img_file.write(image_data)

                        # Add to extracted images list
                        image_info = {
                            'filename': img_filename,
                            'path': str(img_path),
                            'relative_path': f"images/{self.document_name}/{img_filename}",
                            'slide': slide_num + 1,
                            'format': img_ext.upper(),
                            'size_bytes': len(image_data),
                            'source': 'pptx_shape'
                        }
                        images_extracted.append(image_info)
                        self.extracted_images.append(image_info)

            return {
                'success': True,
                'document': str(self.document_path),
                'output_dir': str(self.output_dir),
                'images_count': len(images_extracted),
                'images': images_extracted
            }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error extracting images from PPTX: {str(e)}',
                'images': []
            }

    def _generate_image_filename(self, base_name: str, extension: str) -> str:
        """Generate a unique filename for an image, avoiding collisions"""
        # Clean the base name
        base_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        base_name = base_name.replace(' ', '_')

        filename = f"{base_name}.{extension}"
        counter = 1

        # Check for collisions and add counter if needed
        while (self.output_dir / filename).exists():
            filename = f"{base_name}_{counter}.{extension}"
            counter += 1

        return filename

    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of a file for duplicate detection"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def generate_markdown_references(self, images: List[Dict]) -> str:
        """Generate markdown image references for extracted images"""
        if not images:
            return ""

        markdown_lines = []
        markdown_lines.append("\n## Extracted Images\n")

        for img in images:
            alt_text = f"Image from {img.get('source', 'document')}"
            if 'page' in img:
                alt_text += f" (Page {img['page']})"
            elif 'slide' in img:
                alt_text += f" (Slide {img['slide']})"

            markdown_lines.append(f"![{alt_text}]({img['relative_path']})")
            markdown_lines.append("")  # Empty line for spacing

        return "\n".join(markdown_lines)


def extract_images_from_document(document_path: str, output_dir: str = None) -> Dict:
    """Main function to extract images from a document"""
    try:
        extractor = ImageExtractor(document_path, output_dir)
        result = extractor.extract_images()

        # Add markdown references if images were extracted
        if result['success'] and result['images']:
            result['markdown_references'] = extractor.generate_markdown_references(result['images'])
        else:
            result['markdown_references'] = ""

        return result

    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to extract images: {str(e)}',
            'images': [],
            'markdown_references': ""
        }


def main():
    """Command line interface for image extraction"""
    if len(sys.argv) < 2:
        print("DocuGenius Image Extractor")
        print("Usage: python image_extractor.py <document_path> [output_dir]")
        print("")
        print("Supported formats: PDF, DOCX, PPTX")
        print("Output: JSON with extraction results and image metadata")
        sys.exit(1)

    document_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    # Extract images
    result = extract_images_from_document(document_path, output_dir)

    # Output JSON result
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
