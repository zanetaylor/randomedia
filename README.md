# randomedia

WIP.

Originally developed to work with the [copyparty](https://github.com/9001/copyparty) API.

Now with subfolder ("category") support.

## Config & usage

Create a `.env` file from the template and set:

- `API_ROOT_URL`: the Copyparty API origin, such as `http://copyparty:3923`.
- `FILE_ROOT_URL`: the base URL used by browsers to fetch media files.
- `MEDIA_ROOT`: the path under the API root containing the category directories.
- `MEDIA_DEFAULT_CATEGORY`: a category below `MEDIA_ROOT`.

The app lists categories at `API_ROOT_URL/MEDIA_ROOT`, lists media at `API_ROOT_URL/MEDIA_ROOT/MEDIA_DEFAULT_CATEGORY`, and builds browser media URLs as `FILE_ROOT_URL/MEDIA_ROOT/category/file`. The API must return JSON with a top-level `files` array whose media objects have `href` and `ext` properties.
