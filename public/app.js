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

    let storageRef = firebase.storage().ref('photos/' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15) + " - " + file.name);

    let task = storageRef.put(file);

    task.on('state_changed',

        function progress(snapshot)
        {
            uploader.value = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        },

        function error(err)
        {

        },

        function complete()
        {

        }

    );

});
