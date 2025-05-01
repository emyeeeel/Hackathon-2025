import { Component, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-product-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-input.component.html',
  styleUrl: './product-input.component.scss'
})
export class ProductInputComponent {
  @Output() imageSubmitted = new EventEmitter<{ url?: string, file?: File }>();

  showImageOptions = false;
  selectedOption: 'url' | 'upload' | null = null;
  imageUrl = '';
  selectedFile: File | null = null;
  imagePreviewUrl: string | null = null;
  isDragging = false;

  toggleImageInputOptions() {
    this.showImageOptions = !this.showImageOptions;
    if (!this.showImageOptions) {
      this.resetForm();
    }
  }

  selectImageOption(option: 'url' | 'upload') {
    this.selectedOption = option;
    this.imagePreviewUrl = null;
    this.selectedFile = null;
    this.imageUrl = '';
  }

  submitImageUrl() {
    if (this.imageUrl) {
      this.imagePreviewUrl = this.imageUrl;
      this.imageSubmitted.emit({ url: this.imageUrl });
    }
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.selectedFile = input.files[0];
      this.createImagePreview();
      this.imageSubmitted.emit({ file: this.selectedFile });
    }
  }

  onDragOver(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = true;
  }

  onDragLeave(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
  }

  onDrop(event: DragEvent) {
    event.preventDefault();
    event.stopPropagation();
    this.isDragging = false;
    
    if (event.dataTransfer?.files.length) {
      const file = event.dataTransfer.files[0];
      if (file.type.startsWith('image/')) {
        this.selectedFile = file;
        this.createImagePreview();
        this.imageSubmitted.emit({ file: this.selectedFile });
      }
    }
  }

  createImagePreview() {
    if (this.selectedFile) {
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreviewUrl = e.target?.result as string;
      };
      reader.readAsDataURL(this.selectedFile);
    }
  }

  resetForm() {
    this.selectedOption = null;
    this.imageUrl = '';
    this.selectedFile = null;
    this.imagePreviewUrl = null;
  }
}