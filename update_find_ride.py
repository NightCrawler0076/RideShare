import re

with open("/Users/ramees/Documents/RideShare/find-ride.html", "r") as f:
    content = f.read()

new_script = """    <script type="module">
        import { auth, db } from './firebase-config.js';
        import { onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
        import { collection, addDoc, getDocs, query, orderBy, limit, doc, getDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

        let currentUser = null;
        onAuthStateChanged(auth, (user) => {
            if (!user) {
                window.location.href = 'login.html';
            } else {
                currentUser = user;
                if (window.loadRides) window.loadRides();
            }
        });

        window.handleSignOut = () => {
            signOut(auth).then(() => {
                window.location.href = 'login.html';
            }).catch((error) => {
                console.error("Sign Out Error", error);
            });
        };

        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const htmlElement = document.documentElement;

        if (localStorage.getItem('sharedAppTheme') === 'dark' || (!('sharedAppTheme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            htmlElement.classList.add('dark');
            themeIcon.textContent = 'dark_mode';
        } else {
            htmlElement.classList.remove('dark');
            themeIcon.textContent = 'light_mode';
        }

        themeToggle.addEventListener('click', () => {
            htmlElement.classList.toggle('dark');
            if (htmlElement.classList.contains('dark')) {
                localStorage.setItem('sharedAppTheme', 'dark');
                themeIcon.textContent = 'dark_mode';
            } else {
                localStorage.setItem('sharedAppTheme', 'light');
                themeIcon.textContent = 'light_mode';
            }
        });

        const joinModal = document.getElementById('joinPoolModal');
        const joinModalContent = document.getElementById('joinPoolModalContent');

        window.openJoinModal = () => {
            joinModal.classList.remove('hidden');
            requestAnimationFrame(() => {
                joinModal.classList.remove('opacity-0');
                joinModalContent.classList.remove('scale-95');
                joinModalContent.classList.add('scale-100');
            });
        };

        window.closeJoinModal = () => {
            joinModal.classList.add('opacity-0');
            joinModalContent.classList.remove('scale-100');
            joinModalContent.classList.add('scale-95');
            setTimeout(() => {
                joinModal.classList.add('hidden');
            }, 300);
        };

        window.confirmJoinPool = (btn) => {
            const originalContent = btn.innerHTML;
            btn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span> Sending...';
            btn.disabled = true;

            setTimeout(() => {
                btn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Request Sent!';
                btn.classList.add('bg-green-500', 'hover:bg-green-600');
                btn.classList.remove('bg-theme-primary', 'hover:bg-theme-primary-hover');

                setTimeout(() => {
                    window.closeJoinModal();
                    setTimeout(() => {
                        btn.innerHTML = originalContent;
                        btn.disabled = false;
                        btn.classList.remove('bg-green-500', 'hover:bg-green-600');
                        btn.classList.add('bg-theme-primary', 'hover:bg-theme-primary-hover');
                    }, 300);
                }, 1000);
            }, 800);
        };

        const createModal = document.getElementById('createPoolModal');
        const createModalContent = document.getElementById('createPoolModalContent');

        window.openCreateModal = () => {
            createModal.classList.remove('hidden');
            requestAnimationFrame(() => {
                createModal.classList.remove('opacity-0');
                createModalContent.classList.remove('scale-95');
                createModalContent.classList.add('scale-100');
            });
            const dateInput = createModal.querySelector('input[type="date"]');
            if (dateInput && !dateInput.value) {
                dateInput.valueAsDate = new Date();
            }
        };

        window.closeCreateModal = () => {
            createModal.classList.add('opacity-0');
            createModalContent.classList.remove('scale-100');
            createModalContent.classList.add('scale-95');
            setTimeout(() => {
                createModal.classList.add('hidden');
            }, 300);
        };

        window.adjustSeats = (change) => {
            const input = document.getElementById('seatCount');
            const newValue = parseInt(input.value) + change;
            if (newValue >= 1 && newValue <= 6) {
                input.value = newValue;
            }
        };

        window.adjustLuggage = (change) => {
            const input = document.getElementById('luggageCount');
            const newValue = parseInt(input.value) + change;
            if (newValue >= 0 && newValue <= 4) {
                input.value = newValue;
            }
        };

        window.submitCreatePool = async (btn) => {
            const pickup = document.getElementById('createPickup').value;
            const destination = document.getElementById('createDestination').value;
            const date = document.getElementById('createDate').value;
            const time = document.getElementById('createTime').value;
            const seats = document.getElementById('seatCount').value;
            const cab = document.getElementById('createCab').value;
            const luggage = document.getElementById('luggageCount').value;

            if(!pickup || !destination || !date || !time) {
                alert("Please fill all required fields.");
                return;
            }

            const originalContent = btn.innerHTML;
            btn.innerHTML = '<span class="material-symbols-outlined animate-spin">refresh</span> Creating...';
            btn.disabled = true;

            try {
                let userName = "Student";
                try {
                    const userDoc = await getDoc(doc(db, "users", currentUser.uid));
                    if (userDoc.exists()) userName = userDoc.data().fullName;
                } catch(e) {}

                await addDoc(collection(db, "rides"), {
                    pickup, destination, date, time,
                    seats: parseInt(seats), cab, luggage: parseInt(luggage),
                    creatorName: userName,
                    createdBy: currentUser.uid,
                    createdAt: new Date().toISOString(),
                    status: "active"
                });

                btn.innerHTML = '<span class="material-symbols-outlined">check_circle</span> Pool Created!';
                btn.classList.add('bg-green-500', 'hover:bg-green-600');
                btn.classList.remove('bg-theme-primary', 'hover:bg-theme-primary-hover');

                setTimeout(() => {
                    window.closeCreateModal();
                    window.loadRides();

                    setTimeout(() => {
                        btn.innerHTML = originalContent;
                        btn.disabled = false;
                        btn.classList.remove('bg-green-500', 'hover:bg-green-600');
                        btn.classList.add('bg-theme-primary', 'hover:bg-theme-primary-hover');
                        
                        document.getElementById('createPickup').value = '';
                        document.getElementById('createDestination').value = '';
                        document.getElementById('createTime').value = '';
                        document.getElementById('seatCount').value = '3';
                        document.getElementById('luggageCount').value = '0';
                    }, 300);
                }, 1000);
            } catch (error) {
                console.error("Error creating pool:", error);
                alert("Failed to create pool.");
                btn.disabled = false;
                btn.innerHTML = originalContent;
            }
        };

        window.loadRides = async () => {
            const grid = document.getElementById('ridesGrid');
            try {
                const q = query(collection(db, "rides"), orderBy("createdAt", "desc"), limit(20));
                const querySnapshot = await getDocs(q);
                
                if (querySnapshot.empty) {
                    grid.innerHTML = '<p class="text-theme-muted col-span-full text-center py-10">No active pools found.</p>';
                    return;
                }

                grid.innerHTML = '';
                querySnapshot.forEach((docSnap) => {
                    const ride = docSnap.data();
                    const card = `
                        <div class="bg-theme-surface rounded-xl border border-theme-border overflow-hidden flex flex-col hover:shadow-xl transition-all duration-300">
                            <div class="p-6">
                                <div class="flex justify-between items-start mb-6">
                                    <div class="flex items-center gap-3">
                                        <div class="size-12 rounded-full flex items-center justify-center bg-theme-primary-soft text-theme-primary font-bold text-xl transition-colors duration-300">
                                            ${ride.creatorName ? ride.creatorName[0].toUpperCase() : 'U'}
                                        </div>
                                        <div>
                                            <h3 class="font-bold text-theme-text transition-colors duration-300">${ride.creatorName || 'Student'}</h3>
                                            <div class="flex items-center text-xs text-amber-500 font-bold uppercase transition-colors duration-300">
                                                <span class="material-symbols-outlined text-sm mr-1">star</span> New
                                            </div>
                                        </div>
                                    </div>
                                    <span class="bg-theme-primary-soft text-theme-primary text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider transition-colors duration-300">Active Pool</span>
                                </div>
                                <div class="space-y-4 mb-6">
                                    <div class="flex items-start gap-3">
                                        <div class="flex flex-col items-center mt-1">
                                            <span class="material-symbols-outlined text-theme-primary text-lg transition-colors duration-300">circle</span>
                                            <div class="w-0.5 h-6 bg-theme-divider my-1 transition-colors duration-300"></div>
                                            <span class="material-symbols-outlined text-red-500 text-lg">location_on</span>
                                        </div>
                                        <div class="flex flex-col gap-3">
                                            <div>
                                                <p class="text-xs text-theme-muted font-medium uppercase tracking-tighter transition-colors duration-300">Pickup</p>
                                                <p class="text-sm font-semibold text-theme-heading leading-tight transition-colors duration-300">${ride.pickup}</p>
                                            </div>
                                            <div>
                                                <p class="text-xs text-theme-muted font-medium uppercase tracking-tighter transition-colors duration-300">Destination</p>
                                                <p class="text-sm font-semibold text-theme-heading leading-tight transition-colors duration-300">${ride.destination}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="grid grid-cols-2 gap-4 pt-4 border-t border-theme-border transition-colors duration-300">
                                        <div>
                                            <p class="text-xs text-theme-muted font-medium uppercase mb-1 flex items-center gap-1 transition-colors duration-300">
                                                <span class="material-symbols-outlined text-[14px] text-theme-icon-cyan transition-colors duration-300">schedule</span> Time
                                            </p>
                                            <p class="text-sm font-bold text-theme-heading transition-colors duration-300">${ride.time}</p>
                                        </div>
                                        <div>
                                            <p class="text-xs text-theme-muted font-medium uppercase mb-1 transition-colors duration-300">Date & Seats</p>
                                            <p class="text-sm font-bold text-theme-heading transition-colors duration-300">${ride.date} • ${ride.seats} left</p>
                                        </div>
                                    </div>
                                </div>
                                <button onclick="window.openJoinModal()" class="w-full bg-theme-primary hover:bg-theme-primary-hover text-theme-primary-text font-bold py-3 rounded-lg transition-colors flex items-center justify-center gap-2 duration-300">
                                    Join Pool
                                </button>
                            </div>
                        </div>
                    `;
                    grid.innerHTML += card;
                });
            } catch (error) {
                console.error("Error loading rides:", error);
                grid.innerHTML = '<p class="text-theme-status-red col-span-full text-center py-10">Error loading pools.</p>';
            }
        };
    </script>"""

new_content = re.sub(r'<script type="module">.*?</script>', new_script, content, flags=re.DOTALL)

with open("/Users/ramees/Documents/RideShare/find-ride.html", "w") as f:
    f.write(new_content)
