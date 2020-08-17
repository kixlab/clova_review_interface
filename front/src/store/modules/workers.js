
const state = {
    assignedImages: [],
    annotatedImages: [],
}

const getters = {
    getAssignedImages: (state) => state.assignedImages,
    getAnnotatedImages: (state) => state.annotatedImages,
}

const actions = {
    initalizeImages({ commit }) {
        const fromServer = ['00001', '00002', '00003', '00004']
        const assigned = fromServer.map(function(i) {
            return {
                image_id: i,
                annotated: false,
                start_time: Date(),
                end_time: '',
            }
        })
        console.log("$$ INITIALIZE crowd $$", assigned)
        commit('setAssignedImages', assigned)
    },

    updateAssignedImages({ commit }, images) {
        const annotated = images.filter(v => v.annotated === true)

        commit('setAssignedImages', images)
        commit('setAnnotatedImages', annotated)
    },
}

const mutations = {
    setAssignedImages: (state, assignedImages) => {
        state.assignedImages = assignedImages
    },
    setAnnotatedImages: (state, annotatedImages) => {
        state.annotatedImages = annotatedImages
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}