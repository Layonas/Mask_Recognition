<script lang="ts">
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
// import Camera from "simple-vue-camera";
import { defineComponent, ref } from "vue";
import cam from './components/Camera.vue';
import welcome from './components/Welcome.vue';

export default defineComponent({
    components: {
        cam,
        welcome,
        // HelloWorld,
    },

    setup() {
        // Get a reference of the component
        // const camera = ref<InstanceType<typeof Camera>>();

        // // Use camera reference to call functions
        // const snapshot = async () => {
        //     const blob = await camera.value?.snapshot(
        //         { width: 1920, height: 1080 },
        //         "image/png",
        //         0.5
        //     );
        //     // To show the screenshot with an image tag, create a url
        // };

        // const snap = (blob: Blob) => {
        //     blob.stream
        //     console.log(blob);
        //     console.log("SS taken");
        //     console.log(blob.type);
        //     const url = window.URL.createObjectURL(blob);
        //     console.log(url);
        //     // let link = document.createElement('a');
        //     // link.href = url;
        //     // link.setAttribute('download', 'photo.png');
        //     // link.click();
        //     const el = document.getElementById("image") as HTMLImageElement;
        //     el.src = url;
        //     el.style.visibility = "visible";
        // };

        // // setInterval(()=>{
        // //     snapshot();
        // // }, 500)

        // return {
        //     camera,
        //     snapshot,
        //     snap,
        // };
    },
});
</script>

<template>
    <welcome />
    <cam msg="Your Camera view!"/>
</template>

<style scoped>
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

/* #photo{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    margin-top: 1em;
}

#image {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 75vh;
    height: 42.2vh;
    margin: auto;
    visibility: hidden;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
}

.box {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 75vh;
    height: 42.2vh;
    border: 0.3vh solid rgb(16, 211, 97);
    margin: auto;
    background-color: #1a181867;
}
.camera-box {
    position: relative;
    width: 100%;
    height: 100%;
    margin: auto;
}

#btn{
    position: absolute;
    bottom: 5px;
    right: 40%;
    appearance: none;
    outline: 0;
    background-color: white;
    border: 0;
    padding: 10px 15px;
    color: #53e3a6;
    border-radius: 3px;
    width: 19%;
    cursor: pointer;
    font-size: 13px;
    transition-duration: 0.25s;
}

#btn:hover{
    background-color: #09a4afb6;
}

a {
    color: #42b983;
}

label {
    margin: 0 0.5em;
    font-weight: bold;
}

code {
    background-color: #eee;
    padding: 2px 4px;
    border-radius: 4px;
    color: #304455;
} */
</style>
