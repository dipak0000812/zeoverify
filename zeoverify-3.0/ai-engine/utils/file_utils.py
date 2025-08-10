"""
File utility functions for Zeoverify AI Engine
Handles file validation, processing, and management
"""

import os
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import mimetypes
from datetime import datetime
import shutil

# Supported file formats
SUPPORTED_FORMATS = {
    '.pdf': 'application/pdf',
    '.jpg': 'image/jpeg', 
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.txt': 'text/plain',
    '.doc': 'application/msword',
    '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
}

# Maximum file sizes (in bytes)
MAX_FILE_SIZES = {
    '.pdf': 16 * 1024 * 1024,  # 16MB
    '.jpg': 10 * 1024 * 1024,  # 10MB
    '.jpeg': 10 * 1024 * 1024, # 10MB
    '.png': 10 * 1024 * 1024,  # 10MB
    '.txt': 5 * 1024 * 1024,   # 5MB
    '.doc': 16 * 1024 * 1024,  # 16MB
    '.docx': 16 * 1024 * 1024  # 16MB
}

def validate_file_format(filename: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validate if file format is supported
    
    Args:
        filename: Name of the file to validate
        
    Returns:
        Tuple of (is_valid, error_message, mime_type)
    """
    if not filename:
        return False, "No filename provided", None
    
    # Get file extension
    file_ext = Path(filename).suffix.lower()
    
    if file_ext not in SUPPORTED_FORMATS:
        supported = ", ".join(SUPPORTED_FORMATS.keys())
        return False, f"Unsupported file format. Supported formats: {supported}", None
    
    mime_type = SUPPORTED_FORMATS[file_ext]
    return True, "", mime_type

def validate_file_size(file_path: str, max_size: Optional[int] = None) -> Tuple[bool, str]:
    """
    Validate if file size is within limits
    
    Args:
        file_path: Path to the file
        max_size: Maximum allowed size in bytes (uses default if None)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
    
    # Get file size
    file_size = os.path.getsize(file_path)
    
    # Determine max size based on file extension
    if max_size is None:
        file_ext = Path(file_path).suffix.lower()
        max_size = MAX_FILE_SIZES.get(file_ext, 16 * 1024 * 1024)  # Default 16MB
    
    if file_size > max_size:
        size_mb = file_size / (1024 * 1024)
        max_mb = max_size / (1024 * 1024)
        return False, f"File size ({size_mb:.1f}MB) exceeds maximum allowed size ({max_mb:.1f}MB)"
    
    return True, ""

def get_file_info(file_path: str) -> Dict[str, Any]:
    """
    Get comprehensive information about a file
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary containing file information
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    file_path_obj = Path(file_path)
    
    # Basic file info
    file_info = {
        "filename": file_path_obj.name,
        "extension": file_path_obj.suffix.lower(),
        "size_bytes": os.path.getsize(file_path),
        "size_mb": round(os.path.getsize(file_path) / (1024 * 1024), 2),
        "created_time": datetime.fromtimestamp(os.path.getctime(file_path)).isoformat(),
        "modified_time": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
        "is_file": file_path_obj.is_file(),
        "is_directory": file_path_obj.is_dir()
    }
    
    # MIME type
    mime_type, _ = mimetypes.guess_type(file_path)
    file_info["mime_type"] = mime_type
    
    # File hash (MD5)
    try:
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()
            file_info["md5_hash"] = file_hash
    except Exception as e:
        file_info["md5_hash"] = f"Error: {str(e)}"
    
    # Validation info
    is_valid_format, format_error, _ = validate_file_format(file_path_obj.name)
    is_valid_size, size_error = validate_file_size(file_path)
    
    file_info["validation"] = {
        "format_valid": is_valid_format,
        "format_error": format_error,
        "size_valid": is_valid_size,
        "size_error": size_error,
        "overall_valid": is_valid_format and is_valid_size
    }
    
    return file_info

def save_uploaded_file(uploaded_file, destination_dir: str, 
                       filename: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
    """
    Save an uploaded file to the destination directory
    
    Args:
        uploaded_file: File object from upload
        destination_dir: Directory to save the file
        filename: Optional custom filename
        
    Returns:
        Tuple of (success, message, saved_file_path)
    """
    try:
        # Create destination directory if it doesn't exist
        dest_path = Path(destination_dir)
        dest_path.mkdir(parents=True, exist_ok=True)
        
        # Determine filename
        if filename is None:
            filename = uploaded_file.filename
        
        # Ensure filename is safe
        safe_filename = Path(filename).name  # Remove path components
        
        # Create full file path
        file_path = dest_path / safe_filename
        
        # Check if file already exists
        counter = 1
        original_name = file_path.stem
        original_ext = file_path.suffix
        
        while file_path.exists():
            new_name = f"{original_name}_{counter}{original_ext}"
            file_path = dest_path / new_name
            counter += 1
        
        # Save file
        with open(file_path, 'wb') as f:
            shutil.copyfileobj(uploaded_file.file, f)
        
        # Validate saved file
        is_valid_format, format_error, _ = validate_file_format(str(file_path))
        is_valid_size, size_error = validate_file_size(str(file_path))
        
        if not is_valid_format:
            os.remove(file_path)  # Clean up invalid file
            return False, f"Invalid file format: {format_error}", None
        
        if not is_valid_size:
            os.remove(file_path)  # Clean up oversized file
            return False, f"File size validation failed: {size_error}", None
        
        return True, f"File saved successfully to {file_path}", str(file_path)
        
    except Exception as e:
        return False, f"Error saving file: {str(e)}", None

def cleanup_temp_files(directory: str, max_age_hours: int = 24) -> int:
    """
    Clean up temporary files older than specified age
    
    Args:
        directory: Directory to clean
        max_age_hours: Maximum age of files in hours
        
    Returns:
        Number of files cleaned up
    """
    if not os.path.exists(directory):
        return 0
    
    current_time = datetime.now()
    cleaned_count = 0
    
    try:
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                age_hours = (current_time - file_time).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    try:
                        os.remove(file_path)
                        cleaned_count += 1
                    except Exception as e:
                        print(f"Error removing old file {file_path}: {e}")
    
    except Exception as e:
        print(f"Error during cleanup: {e}")
    
    return cleaned_count

def get_file_extension_from_mime(mime_type: str) -> Optional[str]:
    """
    Get file extension from MIME type
    
    Args:
        mime_type: MIME type string
        
    Returns:
        File extension or None if not found
    """
    # Reverse lookup from SUPPORTED_FORMATS
    for ext, mime in SUPPORTED_FORMATS.items():
        if mime == mime_type:
            return ext
    
    # Fallback to mimetypes module
    ext = mimetypes.guess_extension(mime_type)
    return ext[1:] if ext else None  # Remove leading dot

def is_image_file(file_path: str) -> bool:
    """
    Check if file is an image
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is an image, False otherwise
    """
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    file_ext = Path(file_path).suffix.lower()
    return file_ext in image_extensions

def is_document_file(file_path: str) -> bool:
    """
    Check if file is a document
    
    Args:
        file_path: Path to the file
        
    Returns:
        True if file is a document, False otherwise
    """
    document_extensions = {'.pdf', '.doc', '.docx', '.txt', '.rtf'}
    file_ext = Path(file_path).suffix.lower()
    return file_ext in document_extensions
