# randomedia

WIP.

Originally developed to work with the [copyparty](https://github.com/9001/copyparty) API.

Now with subfolder ("category") support.

## Config & usage

Create a `.env` file from the template with values for your media API endpoint and a default category.

To work out of the box, your media API must return a JSON response with a list of media objects in a top level `files` array. Each media object needs a `href` and `ext` property.
