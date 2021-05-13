const state = {
    imageURL: '',
    imageFile: "logo.png",
    imageBoxes: [],
    imageRatio: '',
    selectedBoxes: [],
    annotatedBoxes: [],
}

const getters = {
    getImageURL: (state) => state.imageURL,
    getImage: (state) => state.imageFile,
    getImageBoxes: (state) => state.imageBoxes,
    getImageRatio: (state) => state.imageRatio,
    getSelectedBoxes: (state) => state.selectedBoxes,
    getAnnotatedBoxes: (state) => state.annotatedBoxes,
    getIfAllBoxesAnnotated: function (state) {
        if (state.imageBoxes.length === 0) {
            return false
        }
        return state.imageBoxes.every(box => box.annotated === true)
    }
}

const actions = {
    /*
    async getImages({ commit }) {
        const response = await axios.get('')
        commit('setImages', response.data)
    },
    */
/* 
    initializeImages({ commit }, name) {
        commit('setCurrImage', name.toString())
    },
 */
    setImage({ commit },docType, id) {
        const imageFile = docType+'/'+docType+"_"+ id.toString() + ".png"
        commit('setCurrImage', imageFile)
    },

    setImageBoxes({ commit }, json) {
        console.log("1. setImageBoxes called, before processed", json)
        const img_w = json[0].meta === undefined ? json[0].image_size.width : json[0].meta.image_size.width
        const img_h = json[0].meta === undefined ? json[0].image_size.width : json[0].meta.image_size.width
        var ratio = 1
        var padding_x = 0
        var padding_y = 0
        if (img_w/json[1] >= img_h/json[2]) {
            ratio = img_w/json[1]
            padding_y = 0//(json[2]-(img_h/ratio))/2
        } else {
            ratio = img_h/json[2]
            padding_x = (json[1]-(img_w/ratio))/2
        }

        commit('setImageRatio', ratio)
        
        if(json[0].valid_line==undefined){
            const validData = json[0]['boxes']
            const processedData = validData.map(function(i) {
            return {box_id: i.box_id,
                    text: i.text,
                    x_pos: i.x[0]/ratio+padding_x, 
                    y_pos: i.y[0]/ratio+padding_y, 
                    x_len: (i.x[1]-i.x[0])/ratio, 
                    y_len: (i.y[2]-i.y[0])/ratio, 
                    selected: false, 
                    annotated: false, 
                    hover: false,
                    quad: {x1: i.x[0], y1: i.y[0], x2: i.x[1], y2: i.y[2], y3: i.y[3]},
                    label: ""}
        })

        commit('setCurrBox', processedData)
        }
        else{
            const validData=json[0].valid_line.map(v => v.words).flat(1)
            const processedData = validData.map(function(i, idx) {
                return {box_id: idx,
                        text: i.text,
                        x_pos: i.quad.x1/ratio+padding_x, 
                        y_pos: i.quad.y1/ratio+padding_y, 
                        x_len: (i.quad.x2-i.quad.x1)/ratio, 
                        y_len: (i.quad.y3-i.quad.y2)/ratio, 
                        selected: false, 
                        annotated: false, 
                        hover: false,
                        quad: {x1: i.quad.x1, y1: i.quad.y1, x2: i.quad.x2, y2: i.quad.y2, y3: i.quad.y3},
                        label: ""}
            })

            console.log("2. setImageBoxes called, processed", processedData)
            commit('setCurrBox', processedData)
            }

    },

    updateImageBoxes({ commit }, json) {
        const selected = json.filter(v => v.selected === true)

        commit('setCurrBox', json)
        commit('setSelectedBox', selected)
        //console.log('BOX_STATUS:', json)
    },

    updateAnnotatedBoxes({ commit }, json) {
        if (json[1] === "add") {
            console.log("Updateannotatedboxes", json);
            commit('addAnnotatedBox', json[0])
        }
        else if (json[1] === "remove") {
            commit('removeAnnotationBox', json[0])
        }
        else if (json[1] === "reset") {
            commit('resetAnnotationBox', [])
        }
    },
}


// The only part where state changes happen
const mutations = {
    setCurrImage: (state, imageFile) => {
        (state.imageFile = imageFile)
        //console.log("New FILE:", state.imageFile)
    },
    setCurrBox: (state, imageBoxes) => {
        console.log("--- IMAGEBOXES JUST CHANGED ---")
        state.imageBoxes = imageBoxes
        //console.log("New JSON:", state.imageBoxes)
    },
    setImageRatio: (state, imageRatio) => {
        state.imageRatio = imageRatio
        //console.log("New RATIO:", state.imageRatio)
    },
    setImageURL: (state, commit, rootState) => {
        console.log(rootState.image_url)
        state.imageURL = rootState.image_url
        //console.log("New RATIO:", state.imageRatio)
    },
    setSelectedBox: (state, selectedBoxes) => {
        state.selectedBoxes = selectedBoxes
        //console.log("NEW SELBOXES:", state.selectedBoxes)
    },
    addAnnotatedBox: (state, annotatedBoxes) => {
        state.annotatedBoxes.push(annotatedBoxes)
        //console.log("ANNOTATED:", state.annotatedBoxes)
    },
    removeAnnotationBox: (state, annotatedBoxes) => {
        state.annotatedBoxes.splice(state.annotatedBoxes.indexOf(annotatedBoxes), 1)
        //console.log("REMOVED:", state.annotatedBoxes)
    },
    resetAnnotationBox: (state, annotatedBoxes) => {
        state.annotatedBoxes = annotatedBoxes
        // console.log(state.annotatedBoxes)
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}