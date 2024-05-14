from huggingface_hub import snapshot_download

## when need to login huggingface for login

# from huggingface_hub import login
# login()

snapshot_download(
  repo_id="liuhaotian/llava-v1.5-13b",
  # repo_type="dataset",
  local_dir="/xxx/local_dir", # download files to here
  local_dir_use_symlinks=False, # avoid download to cache
  max_workers=8
)