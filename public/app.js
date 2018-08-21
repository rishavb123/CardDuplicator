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

    let task = storageRef.put(file);

    task.on('state_changed',

        function progress(snapshot)
        {
            let percent = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
            uploader.value = percent;
        },

        function error(err)
        {

        },

        function complete()
        {

        }

    );

});
