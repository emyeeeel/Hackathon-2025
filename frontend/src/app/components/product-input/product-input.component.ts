import { Component, Output, EventEmitter, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpEventType } from '@angular/common/http';

@Component({
  selector: 'app-product-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './product-input.component.html',
  styleUrls: ['./product-input.component.scss']
})
export class ProductInputComponent {
  @Output() imageSubmitted = new EventEmitter<{ url?: string, file?: File }>();
  @Input() identifiedProduct: any; // Input property to receive data from parent
  
  showImageOptions = false;
  selectedOption: string | null = 'upload';
  imageUrl: string = '';
  selectedFile: File | null = null;
  imagePreviewUrl: string | null = null;
  isDragging = false;
  uploadProgress: number = 0;
  urlUploadProgress: number = 0; // Progress for URL input
  isUploadComplete: boolean = false; // New flag to track upload completion

  constructor(private http: HttpClient) {}

  selectImageOption(option: 'url' | 'upload') {
    this.selectedOption = option;
    this.resetProgress(); // Reset progress and related variables
    this.imageUrl = ''; // Clear the URL input field
    this.selectedFile = null; // Clear the selected file
  }

  submitImageUrl() {
    if (!this.imageUrl) {
      alert('Please enter a valid image URL.');
      return;
    }

    this.urlUploadProgress = 0;
    this.imagePreviewUrl = null;

    // Simulate URL loading progress
    const interval = setInterval(() => {
      if (this.urlUploadProgress < 100) {
        this.urlUploadProgress += 10; // Increment progress
      } else {
        clearInterval(interval);
        this.imagePreviewUrl = this.imageUrl; // Set the preview URL
        console.log('URL loading complete');
        console.log(this.identifiedProduct)
      }
    }, 100); // Simulate loading speed

    console.log('Sending URL to backend:', this.imageUrl);
    this.imageSubmitted.emit({ url: this.imageUrl }); // Emit the URL
  }

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files?.length) {
      this.selectedFile = input.files[0];
      this.imagePreviewUrl = URL.createObjectURL(this.selectedFile); // Set preview URL for file
      this.imageSubmitted.emit({ file: this.selectedFile });
      this.uploadFile(this.selectedFile);

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
        this.imagePreviewUrl = URL.createObjectURL(this.selectedFile); // Set preview URL for file
        this.imageSubmitted.emit({ file: this.selectedFile });
        this.uploadFile(this.selectedFile);
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

  uploadFile(file: File) {
    this.uploadProgress = 0;
    this.isUploadComplete = false; // Reset the flag when a new upload starts
    const totalSize = file.size;
    const chunkSize = totalSize / 100;
    let uploadedSize = 0;

    const interval = setInterval(() => {
      if (uploadedSize < totalSize) {
        uploadedSize += chunkSize;
        this.uploadProgress = Math.min(Math.round((uploadedSize / totalSize) * 100), 100);
      } else {
        clearInterval(interval);
        console.log('Simulated upload complete');
        this.uploadProgress = 100;
        this.isUploadComplete = true; // Set the flag when upload is complete
      }
    }, 50);
  }

  resetForm() {
    this.selectedOption = null;
    this.imageUrl = '';
    this.selectedFile = null;
    this.imagePreviewUrl = null;
    this.isUploadComplete = false; // Reset the flag when the form is reset
  }

  resetProgress() {
    console.log('Resetting progress...');
    this.uploadProgress = 0;
    this.urlUploadProgress = 0; // Reset URL progress
    this.identifiedProduct = null; // Clear identified product details
    this.imagePreviewUrl = null; // Clear image preview
    this.isUploadComplete = false; // Reset upload completion flag
  }
}