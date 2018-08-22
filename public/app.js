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

    let storageRef = firebase.storage().ref('photos/' + file.name);

    firebase.database().ref("job").once("value", snap => {
        if(snap.val() === "complete" || !snap.val())
        {
            firebase.database().ref("job").set("new job");
            let task = storageRef.put(file);
            task.on('state_changed',

                //on progress
                snapshot => {
                    uploader.value = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
                },

                err => {}, // on error

                () => {
                    location.href="veiwer.html"
                } // on complete

            );
        }
        else
        {
            alert("Another Job is in process\nTry Again in 1-2 minutes")
        }
    })

});
