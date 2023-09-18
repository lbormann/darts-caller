function toggleCheckout(playerId) {
    var checkout = document.getElementById("checkout" + playerId);
    if (checkout.style.display === "none" || checkout.style.display === "") {
        checkout.classList.remove("animate__fadeOutRight");
        checkout.classList.add("animate__fadeInRight");
        checkout.style.display = "table";
    } else {
        checkout.classList.remove("animate__fadeInRight");
        checkout.classList.add("animate__fadeOutRight");
        checkout.addEventListener("animationend", function () {
            checkout.style.display = "none";
        }, { once: true });
    }
}

function toggleStats() {
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
function toggleAverage() {
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

