<script lang="ts">
import { defineComponent, PropType, ref } from "vue";
import Camera from 'simple-vue-camera';
import axios from 'axios'

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

    // if(!camera.value){
    //   return alert("Something went wrong with camera, please try choosing the camera or refresh page.");
    // }

    let MenuActive = ref(false);
    let interval = ref(0);
    let ss_interval = ref(0);

    const loading = async () =>{

      const devices = await camera.value?.devices(["videoinput"]);

      console.log("Loading");

      if(!devices){
        return alert("No camera devices loaded!");
      }

      if(devices.length <= 0) {
        return alert("No devices found! Please try to refresh or choose a valid camera device!");
      }
    }


    const started = () =>{
      console.log("Video started!");
    }

        // Use camera reference to call functions
        const snapshot = async () => {

          if(interval.value == 1){
            interval.value = 2;
            //means it needs to be stopped;
          }

          if(interval.value == 0){

            ss_interval.value = setInterval(async () => {
              const blob = await camera.value?.snapshot(
                  { width: 854, height: 480 },
                  "image/png",
                  0.01
              );
              // To show the screenshot with an image tag, create a url
            }, 1000/5);

            const start_button = document.getElementById("btn") as HTMLButtonElement;
            start_button.textContent = "Stop recognition";

            interval.value = 1;
          }

          if(interval.value == 2){
            clearInterval(ss_interval.value);
            ss_interval.value = 0;
            interval.value = 0;
            const start_button = document.getElementById("btn") as HTMLButtonElement;
            start_button.textContent = "Start recognition";
          }
        };

        const snap = (blob: Blob) => {
          
            //console.log(blob);
            //blob.stream;
            //console.log("SS taken");
            //console.log(blob.type);

            //const url = window.URL.createObjectURL(blob);

            var reader = new FileReader();
            reader.readAsDataURL(blob);

            reader.onloadend = function() {

              var base64data = reader.result;
              //console.log(base64data)

              axios.post('http://127.0.0.1:5000/predict',{ // this will change if deployed online
                blob: base64data
              }).then((response) => { // response is base64 string

                //console.log(url);
                //console.log(response);
                const base64 = "data:image/png;base64," + response.data;
                //console.log(base64);

                //console.log(reader.readAsDataURL(base64));

                // let link = document.createElement('a');
                // link.href = url;
                // link.setAttribute('download', 'photo.png');
                // link.click();

                //return console.log(response.data);
                const el = document.getElementById("image") as HTMLImageElement;
                el.src = base64;
                el.style.visibility = "visible";

              })
            }
            
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

          let ul = document.getElementById("devices") as HTMLUListElement;
          
          if(ul.childElementCount !== devices.length){

            for(var i = 0; i < devices.length; i++){
              let li = document.createElement("li") as HTMLLIElement;
              let h2 = document.createElement("h2");
              h2.addEventListener('click', async function(id){
                const devices = await camera.value?.devices(["videoinput"]);
  
                if (!devices)
                  return alert('No devices!');

                const items = ul.getElementsByTagName('li');

                for(var i = 0; i < items.length; i++){
                  const item = items[i] as HTMLLIElement;
                  if(h2.innerText !== item.getElementsByTagName('h2')[0].innerText)
                    item.style.borderLeftColor = 'rgba(166, 44, 43, 0.8)';
                }
  
                for(var i = 0; i < devices.length; i++){
                  if(devices[i].label === h2.innerText){
                    camera?.value?.changeCamera(devices[i].deviceId);
                    li.style.borderLeftColor = 'rgba(0, 209, 80, 0.8)'
                  }
                }
              });
              h2.innerText = devices[i].label;
              li.appendChild(h2);
              li.setAttribute("class", "device_list");
              li.style.paddingLeft = '4px'
              li.style.borderLeft = '6px solid rgba(166, 44, 43, 0.8)'
              li.style.listStyleType = 'none';
              ul.appendChild(li);
            }
            
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
                    :resolution="{ width: 854, height: 480 }"
                    ref="camera"
                    @loading="loading"
                    @camera-change="ChangeCameraEvent"
                    @started="started"
                    @snapshot="snap"
                    autoplay
                >
                <button @click="snapshot" id="btn">Start recognition</button>
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