<template>
    <v-container fluid fill-height>
        <v-row justify="center">
            <v-btn-toggle v-model="toggle_exclusive" class="py-2" color="indigo">
                <v-btn depressed style="margin: 0 0px; text-transform: lowercase">
                    <span><b><b>N/A</b></b> resolution</span>
                </v-btn>
                <v-btn depressed style="margin: 0 0px; text-transform: lowercase">
                    <span><b><b>Close to</b></b> resolution</span>
                </v-btn>
            </v-btn-toggle>
        </v-row>

        <v-row style="border: 1px solid black; height: 85vh">
            <v-col cols="9" style="border: 1px solid black;">
                <template v-if="toggle_exclusive === 0">
                    <na-resolution/>
                </template>
                <template v-else-if="toggle_exclusive === 1">
                    <close-to-resolution/>
                </template>
                <template v-else>
                    <h2 style="margin: 20px 0;">Please select one of the two resolutions to begin.</h2>
                </template>
            </v-col>
            <v-col cols="3" style="border: 1px solid black;">
                Resulting label set & annotation
            </v-col>
        </v-row>

    </v-container>
</template>

<script>
import NaResolution from '@/components/NaResolution.vue'
import CloseToResolution from '@/components/CloseToResolution.vue'
export default {
    name: "Dashboard",
    components: {
        NaResolution,
        CloseToResolution
    },
    data() {
        return {
            toggle_exclusive: null,
        }
    },
}
</script>

<style scoped>

</style>