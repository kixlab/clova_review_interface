//import axios from 'axios'
import json from '../../assets/receipt_00001.json';

const state = {
    imageFile: "logo.png",
    imageBoxes: [],
    imageRatio: '',
    selectedBoxes: [],
}

const getters = {
    getImage: (state) => state.imageFile,
    getImageBoxes: (state) => state.imageBoxes,
    getImageRatio: (state) => state.imageRatio,
    getSelectedBoxes: (state) => state.selectedBoxes,
}

const actions = {
    /*
    async getImages({ commit }) {
        const response = await axios.get('')
        commit('setImages', response.data)
    },
    */

    initializeImages({ commit }, name) {
        commit('setCurrImage', name.toString())
    },

    setImage({ commit }, id) {
        //const imageBoxes = "receipt_" + id.toString() + ".json"
        const imageFile = "receipt_" + id.toString() + ".png"
        commit('setCurrImage', imageFile)
        //commit('setCurrBox', imageBoxes)
    },

    setImageBoxes({ commit }, id) {
        console.log("ID:", id)

        const img_w = json.meta.image_size.width
        const img_h = json.meta.image_size.height
        var ratio = 1
        var padding_x = 0
        var padding_y = 0
        if (img_w/400 >= img_h/500) {
            ratio = img_w/400
            padding_y = (500-(img_h/ratio))/2
        } else {
            ratio = img_h/500
            padding_x = (400-(img_w/ratio))/2
        }
        //console.log("padding_x:", padding_x/ratio, ", padding_y:", padding_y/ratio)
        //const ratio = Math.max(img_w/400, img_h/500)

        commit('setImageRatio', ratio)
        

        const validData = json.valid_line.map(v => v.words).flat(1)
        const processedData = validData.map(function(i) {
            return {id: i.row_id, text: i.text, x_pos: i.quad.x1/ratio+padding_x, y_pos: i.quad.y1/ratio+padding_y, x_len: (i.quad.x2-i.quad.x1)/ratio, y_len: (i.quad.y3-i.quad.y2)/ratio, selected: false, annotated: false, label: ""}
        })
        
        commit('setCurrBox', processedData)
    },

    updateImageBoxes({ commit }, json) {
        const selected = json.filter(v => v.selected === true)

        commit('setCurrBox', json)
        commit('setSelectedBox', selected)
    }

}


// The only part where state changes happen
const mutations = {
    setCurrImage: (state, imageFile) => {
        (state.imageFile = imageFile)
        //console.log("New FILE:", state.imageFile)
    },
    setCurrBox: (state, imageBoxes) => {
        state.imageBoxes = imageBoxes
        //console.log("New JSON:", state.imageBoxes)
    },
    setImageRatio: (state, imageRatio) => {
        state.imageRatio = imageRatio
        //console.log("New RATIO:", state.imageRatio)
    },
    setSelectedBox: (state, selectedBoxes) => {
        state.selectedBoxes = selectedBoxes
        //console.log("NEW SELBOXES:", state.selectedBoxes)
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}