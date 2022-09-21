// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getStorage } from "firebase/storage";
import { getFirestore } from "firebase/firestore";
import { getDatabase } from "firebase/database";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration

console.log("firebase innnnnnnnnnnnnnnn")
export const firebaseConfig = {
    apiKey: "AIzaSyB3UHqcSKu-XQOmQzOjGjKGFUp7nTrffCU",
    authDomain: "grouplisten.firebaseapp.com",
    projectId: "grouplisten",
    storageBucket: "grouplisten.appspot.com",
    messagingSenderId: "570913591007",
    appId: "1:570913591007:web:3f4ef799fa17c8e23a636a"
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);


export const storage = getStorage(firebaseApp);
export const db = getFirestore(firebaseApp);
export const database = getDatabase(firebaseApp);

export default firebaseApp;