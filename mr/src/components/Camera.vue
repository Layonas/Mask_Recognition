<script lang="ts">
import { defineComponent, PropType, ref } from "vue";
import Camera from 'simple-vue-camera';

export default defineComponent({
  components:{
    Camera,
  },
  props: {
    msg:{
      required: true,
      type: String
    }
  },
  setup(){

    const camera = ref<InstanceType<typeof Camera>>();

    console.log(camera);

    let MenuActive = ref(false);

    const loading = async () =>{
      const devices = await camera.value?.devices(["videoinput"]);
      console.log("Loading");
      console.log(this);

      if(devices.length <= 0) {
        alert("No devices found");
      }
    }

    const started = () =>{
      console.log("Video started!");
    }

        // Use camera reference to call functions
        const snapshot = async () => {
            const blob = await camera.value?.snapshot(
                { width: 1280, height: 720 },
                "image/png",
                0.5
            );
            // To show the screenshot with an image tag, create a url
        };

        const snap = (blob: Blob) => {
            blob.stream
            console.log(blob);
            console.log("SS taken");
            console.log(blob.type);
            const url = window.URL.createObjectURL(blob);
            console.log(url);
            // let link = document.createElement('a');
            // link.href = url;
            // link.setAttribute('download', 'photo.png');
            // link.click();
            const el = document.getElementById("image") as HTMLImageElement;
            el.src = url;
            el.style.visibility = "visible";
        };

        const ChangeCameraEvent = async (id : string) =>{
          const devices = await camera.value?.devices(["videoinput"]);

          if(!devices)
            return;

          let name = "";

          for(var i = 0; i < devices.length; i++){
            if(devices[i].deviceId === id)
              name = devices[i].label;
          }

          console.log("Camera changed to: " + name);
        }

        const click = async () => {
          const devices = await camera.value?.devices(["videoinput"]);

          if (!devices)
            return alert('No devices!');

          console.log(devices);

          let ul = document.getElementById("devices") as HTMLUListElement;

          for(var i = 0; i < devices.length; i++){
            let li = document.createElement("li") as HTMLLIElement;
            let h2 = document.createElement("h2");
            h2.addEventListener('click', async function(id){
              const devices = await camera.value?.devices(["videoinput"]);

              if (!devices)
                return alert('No devices!');

              for(var i = 0; i < devices.length; i++)
                if(devices[i].label === h2.innerText)
                  camera?.value?.changeCamera(devices[i].deviceId);
            });
            h2.innerText = devices[i].label;
            li.appendChild(h2);
            ul.appendChild(li);
          }

          let w = document.getElementById("camera-selector") as HTMLDivElement;
          w.classList.add("inactive");
          let overlay = document.getElementById("overlay1") as HTMLDivElement;
          overlay.classList.add("inactive");
        };

        const unclick = () => {
          let w = document.getElementById("camera-selector") as HTMLDivElement;
            w.classList.remove("inactive");
            let overlay = document.getElementById("overlay1") as HTMLDivElement;
            overlay.classList.remove("inactive");
        }


        return {
          camera,
          loading,
          snapshot,
          snap,
          started,
          ChangeCameraEvent,
          click,
          unclick,
          MenuActive,
        }

  },
});  



</script>

<template>
<!-- <CameraSelectorVue :camera="camera" /> -->
<h1>{{msg}}</h1>
    <div class="container">
        <div class="box">
            <div class="camera-box">
                <camera
                    :resolution="{ width: 1280, height: 720 }"
                    ref="camera"
                    @loading="loading"
                    @camera-change="ChangeCameraEvent"
                    @started="started"
                    @snapshot="snap"
                    autoplay
                >
                <button @click="snapshot" id="btn">Create Snapshot</button>
                <button class="camera-button" @click="click"></button>
                </camera>
            </div>
        </div>
    </div>
    <div id="photo">
        <img src="" alt="ss" id="image" />
    </div>

        <div class="camera-selector" id="camera-selector">
        <div class="header">
            <div class="title">Camera selector</div>
            <button class="close-button" @click="unclick">&times;</button>
        </div>
        <div class="body">
            <ul id="devices">
            </ul>
        </div>
    </div>
    <div id="overlay1" @click="unclick"></div>

</template>

<style scoped>

#photo{
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

.camera-button{
    background-image: url('../assets/camera.png');
    position: absolute;
    background-repeat: no-repeat;
    background-color: rgba(0, 0, 0, 0.3);
    background-size:cover;
    bottom: 5px;
    right: 32%;
    appearance: none;
    outline: 0;
    border: 0;
    padding: 10px 15px;
    border-radius: 3px;
    width: 40px;
    height: 38px;
    cursor: pointer;
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
}

.camera-selector {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(0);
    transition: 300ms ease-in-out;
    border: 1px solid black;
    border-radius: 10px;
    z-index: 9;
    background-color: aquamarine;
    width: 500px;
    max-width: 80%;
}

.camera-selector.inactive {
    transform: translate(-50%, -50%) scale(1);
}

.header {
    padding: 10px 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid black;
}

.title {
    font-size: 1.25rem;
    font-weight: bold;
}

.close-button {
    cursor: pointer;
    border: none;
    outline: none;
    background: none;
    font-size: 1.25rem;
    font-weight: bold;
}

.body {
    padding: 10px 15px;
    text-align: left;
}

#overlay1 {
    position: fixed;
    opacity: 0;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    pointer-events: none;
    transition: 300ms ease-in-out;
    z-index: 4;
}

#overlay1.inactive {
    opacity: 1;
    pointer-events: all;
}
</style>