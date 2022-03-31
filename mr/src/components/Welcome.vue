<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
    setup() {
        const click = () => {
            let w = document.getElementById("welcome") as HTMLDivElement;
            w.classList.add("inactive");
            let overlay = document.getElementById("overlay") as HTMLDivElement;
            overlay.classList.add("inactive");
        };

        return {
            click,
        };
    },
});
</script>

<template>
    <div class="welcome" id="welcome">
        <div class="header">
            <div class="title">Welcome</div>
            <button class="close-button" @click="click">&times;</button>
        </div>
        <div class="body">
            This is a university project to capture and print out results whether a person is
            wearing a mask or not. <br />To use this website you will need to allow camera access
            and if camera is incorrect choose a camera that would work. <br />By using this website
            you take full responsibility for any actions you take.
        </div>
    </div>
    <div id="overlay" @click="click"></div>
</template>

<style scoped>
.welcome {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) scale(1);
    transition: 300ms ease-in-out;
    border: 1px solid black;
    border-radius: 10px;
    z-index: 10;
    background-color: aquamarine;
    width: 500px;
    max-width: 80%;
}

.welcome.inactive {
    transform: translate(-50%, -50%) scale(0);
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

#overlay {
    position: fixed;
    opacity: 1;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    pointer-events: all;
    transition: 300ms ease-in-out;
    z-index: 5;
}

#overlay.inactive {
    opacity: 0;
    pointer-events: none;
}
</style>
