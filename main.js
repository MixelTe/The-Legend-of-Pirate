const pirate_swim = document.getElementById("pirate-swim");
const pirate_swim_img = pirate_swim.firstElementChild

function anim()
{
	const topScreen = pirate_swim.getBoundingClientRect().top;
	const top = pirate_swim.offsetTop;
	const width = pirate_swim.offsetWidth
	const widthImd = pirate_swim_img.offsetWidth
	const v = (1 - topScreen / top) * (width - widthImd);
	pirate_swim_img.style.left = `${Math.min(width - widthImd, Math.max(0, v))}px`
}
window.addEventListener("scroll", anim);
anim();