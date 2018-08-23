// Initialize Firebase
let config = {
    apiKey: "AIzaSyBG8Vxk1MsP2bEZsOpe4cJYrIbqkGbFHZE",
    authDomain: "card-duplicator.firebaseapp.com",
    databaseURL: "https://card-duplicator.firebaseio.com",
    projectId: "card-duplicator",
    storageBucket: "card-duplicator.appspot.com",
    messagingSenderId: "70748670873"
};
firebase.initializeApp(config);

let uploader = document.getElementById('progress');
let fileButton = document.getElementById('cameraInput');

fileButton.addEventListener('change', e => {

    let file = e.target.files[0];

    let storageRef = firebase.storage().ref(file.name);

    firebase.database().ref("server").once("value", snap => {
        if(snap.val() === "on")
        firebase.database().ref("job").once("value", snap => {
            if(snap.val() === "complete" || !snap.val())
            {
                firebase.database().ref("job").set("start");
                let task = storageRef.put(file);
                task.on('state_changed',

                    //on progress
                    snapshot => {
                        uploader.value = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                    },

                    err => {}, // on error

                    () => {
                        firebase.database().ref("job").on("value", snap => {
                            if(snap.val() === "complete")
                                location.href="viewer.html";
                        });
                    } // on complete

                );
            }
            else
            {
                alert("Another Job is in process\nTry Again in 1-2 minutes");
            }
        });
        else
            alert("Server is off");
    });

});
