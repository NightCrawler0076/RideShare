// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-analytics.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/12.11.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBU3DCw_1xhGZ01kTRG-8mjL4gAkhityeg",
  authDomain: "rideshare-6ee7f.firebaseapp.com",
  projectId: "rideshare-6ee7f",
  storageBucket: "rideshare-6ee7f.firebasestorage.app",
  messagingSenderId: "859446769851",
  appId: "1:859446769851:web:04bb9f3b197d732b9f919e",
  measurementId: "G-409NLD129V"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, analytics, auth, db };
