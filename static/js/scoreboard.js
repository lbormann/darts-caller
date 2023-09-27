function toggleStatsTable() {
    var statsTable = document.getElementById("statsTable");
    if (statsTable.style.display === "none" || statsTable.style.display === "") {
        statsTable.classList.remove("animate__fadeOutRight");
        statsTable.classList.add("animate__fadeInRight");
        statsTable.style.display = "table";
    } else {
        statsTable.classList.remove("animate__fadeInRight");
        statsTable.classList.add("animate__fadeOutRight");

        statsTable.addEventListener("animationend", function () {
            statsTable.style.display = "none";
        }, { once: true });
    }
}
function toggleAverageTable() {
    var averageTable = document.getElementById("averageTable");
    if (averageTable.style.display === "none" || averageTable.style.display === "") {
        averageTable.classList.remove("animate__fadeOutRight");
        averageTable.classList.add("animate__fadeInRight");
        averageTable.style.display = "table";
    } else {
        averageTable.classList.remove("animate__fadeInRight");
        averageTable.classList.add("animate__fadeOutRight");

        averageTable.addEventListener("animationend", function () {
            averageTable.style.display = "none";
        }, { once: true });
    }
}
function toggleCheckout1() {
    var checkout1 = document.getElementById("checkout1");
    if (checkout1.style.display === "none" || checkout1.style.display === "") {
        checkout1.classList.remove("animate__fadeOutRight");
        checkout1.classList.add("animate__fadeInRight");
        checkout1.style.display = "table";
    } else {
        checkout1.classList.remove("animate__fadeInRight");
        checkout1.classList.add("animate__fadeOutRight");

        checkout1.addEventListener("animationend", function () {
            checkout1.style.display = "none";
        }, { once: true });
    }
}

function toggleCheckout1_darter() {
	var darter = document.getElementById("player1checkout_darter");
	if (darter.style.display === "none") {
		darter.style.display = "";
	} else {
		darter.style.display = "none";
	}
}

function toggleCheckout1_possible1() {
	var tog = document.getElementById("player1checkout_possible1");
	if (tog.style.display === "none") {
		tog.style.display = "";
	} else {
		tog.style.display = "none";
	}
}

function toggleCheckout1_possible2() {
	var tog = document.getElementById("player1checkout_possible2");
	if (tog.style.display === "none") {
		tog.style.display = "";
	} else {
		tog.style.display = "none";
	}
}

function toggleCheckout1_possible3() {
	var tog = document.getElementById("player1checkout_possible3");
	if (tog.style.display === "none") {
		tog.style.display = "";
	} else {
		tog.style.display = "none";
	}
}

function toggleArrow() {
	var arrow1 = document.getElementById("arrow1");
	var arrow2 = document.getElementById("arrow2");
	if (arrow2.style.visibility === "hidden") {
		arrow2.style.visibility = "visible";
		arrow1.style.visibility = "hidden";
	} else {
		arrow1.style.visibility = "visible";
		arrow2.style.visibility = "hidden";
	}
}

function toggleCheckout2() {
    var checkout2 = document.getElementById("checkout2");
    if (checkout2.style.display === "none" || checkout2.style.display === "") {
        checkout2.classList.remove("animate__fadeOutRight");
        checkout2.classList.add("animate__fadeInRight");
        checkout2.style.display = "table";
    } else {
        checkout2.classList.remove("animate__fadeInRight");
        checkout2.classList.add("animate__fadeOutRight");

        checkout2.addEventListener("animationend", function () {
            checkout2.style.display = "none";
        }, { once: true });
    }
}

function toggleCheckout2_darter() {
	var darter = document.getElementById("player2checkout_darter");
	if (darter.style.display === "none") {
		darter.style.display = "";
	} else {
		darter.style.display = "none";
	}
}

function toggleCheckout2_possible1() {
	var tog = document.getElementById("player2checkout_possible1");
	if (tog.style.display === "none") {
		tog.style.display = "";
	} else {
		tog.style.display = "none";
	}
}

function toggleCheckout2_possible2() {
	var tog = document.getElementById("player2checkout_possible2");
	if (tog.style.display === "none") {
		tog.style.display = "";
	} else {
		tog.style.display = "none";
	}
}

function toggleCheckout2_possible3() {
	var tog = document.getElementById("player2checkout_possible3");
	if (tog.style.display === "none") {
		tog.style.display = "";
	} else {
		tog.style.display = "none";
	}
}

function toggleArrowText() {
    var arrow1 = document.getElementById("arrow1");
    var arrow2 = document.getElementById("arrow2");

        arrow1.innerHTML = "180";
        arrow2.innerHTML = "180";
        arrow1.classList.add("animate__heartBeat");
        arrow2.classList.add("animate__heartBeat");

        setTimeout(function () {
			arrow1.classList.remove("animate__heartBeat");
			arrow2.classList.remove("animate__heartBeat");
            arrow1.innerHTML = "&#x25c4;";
            arrow2.innerHTML = "&#x25c4;";
			toggleArrow();
        }, 2000); // Adjust the timing as needed
}

