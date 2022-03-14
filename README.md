# Suggestion Review Interface
This interface is used as a part of the funded project with Clova, to review label suggestions made by annotators (interface available [here](https://github.com/kixlab/clova_annotation_interface)) and finalize the dataset.

## Structure
* Frontend (`/front`): Vue.js
  * Codes for different pages are in the [views](./src/views) folder, in the order of -
    * [Landing.vue](./src/views/Landing.vue)
    * [Dashboard.vue](./src/views/Dashboard.vue)
    * [ImageView.vue](./src/views/ImageView.vue) - this file is used to show the raw data


  * The [components](./src/components) folder has Vue files of the components in each page, and the [assets](./src/assets) folder contains instructions and images.

