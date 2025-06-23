// SPDX-License-Identifier: (Apache-2.0 OR MIT)

use crate::ffi::ImageUrl;
use crate::serialize::error::SerializeError;
use crate::str::unicode_to_str;
use crate::typeref::STR_TYPE;

use base64::prelude::*;
use serde::ser::{Serialize, Serializer};

#[repr(transparent)]
pub struct ImageUrlSerializer {
    ptr: *mut pyo3_ffi::PyObject,
}

impl ImageUrlSerializer {
    pub fn new(ptr: *mut pyo3_ffi::PyObject) -> Self {
        ImageUrlSerializer { ptr: ptr }
    }
}

impl Serialize for ImageUrlSerializer {
    #[cold]
    #[inline(never)]
    #[cfg_attr(feature = "optimize", optimize(size))]
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        unsafe {
            let imageurl: *mut ImageUrl = self.ptr as *mut ImageUrl;
            let url_obj = (*imageurl).url;
            
            // Extract URL string from Python object
            let ob_type = ob_type!(url_obj);
            if ob_type != STR_TYPE {
                err!(SerializeError::InvalidStr)
            }
            
            let url_str = unicode_to_str(url_obj);
            if unlikely!(url_str.is_none()) {
                err!(SerializeError::InvalidStr)
            }
            
            let url = url_str.unwrap();
            
            // Fetch image and convert to base64
            let base64_data = match fetch_and_encode_image(url) {
                Ok(data) => data,
                Err(_) => {
                    // If fetching fails, return an error or empty string
                    return serializer.serialize_str("");
                }
            };
            
            serializer.serialize_str(&base64_data)
        }
    }
}

fn fetch_and_encode_image(url: &str) -> Result<String, Box<dyn std::error::Error + Send + Sync>> {
    // Create a simple runtime for the async operation
    let rt = tokio::runtime::Builder::new_current_thread()
        .enable_all()
        .build()?;
    
    rt.block_on(async {
        // Fetch the image
        let response = reqwest::get(url).await?;
        let bytes = response.bytes().await?;
        
        // Encode to base64
        let base64_string = base64::prelude::BASE64_STANDARD.encode(&bytes);
        
        // Return data URL format
        Ok(format!("data:image/jpeg;base64,{}", base64_string))
    })
}
