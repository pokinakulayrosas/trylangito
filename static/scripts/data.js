const mapClasses = [
    "variant-1",
    "variant-2",
    "variant-3",
    "variant-1",
    "variant-2",
    "variant-3",
    "variant-1",
    "variant-2",
    "variant-3",
    "variant-1",
  ];
const previews = [
    {
      img: "./static/assets/2.png",
      title: "Joy",
      tags: "One of the basic emotions",
      description:
        "A pleasurable or satisfying experience",
    },
    {
      img: "./static/assets/1.png",
      title: "Sadness",
      tags: "One of the basic emotions",
      description:
        "Affected with or expressive of grief or unhappiness ",
    },
    {
      img: "./static/assets/3.png",
      title: "Anger",
      tags: "One of the basic emotions",
      description:
        "A strong feeling of displeasure and usually of antagonism",
    },
    {
      img: "./static/assets/4.png",
      title: "Fear",
      tags: "One of the basic emotions",
      description:
        "An unpleasant often strong emotion caused by anticipation or awareness of danger",
    },
    {
      img: "./static/assets/5.png",
      title: "Disgust",
      tags: "One of the basic emotions",
      description:
        "Marked aversion aroused by something highly distasteful",
    }
  ];
  

document.addEventListener("DOMContentLoaded", function () {
  const container = document.querySelector(".container");
  const previewBg = document.querySelector(".preview-bg");
  const items = document.querySelectorAll(".item");
  let activePreview = document.querySelector(".preview.default");

  let isMouseOverItem = false;

  const defaultClipPaths = {
    "variant-1": "polygon(0% 100%, 100% 100%, 100% 100%, 0% 100%)",
    "variant-2": "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)",
    "variant-3": "polygon(0% 0%, 0% 0%, 0% 100%, 0% 100%)",
  };

  const variantTransforms = {
    "variant-1": {
      title: { x: 75, opacity: 0 },
      tags: { y: -75, opacity: 0 },
      description: { x: -75, opacity: 0 },
    },
    "variant-2": {
      title: { x: -75, opacity: 0 },
      tags: { y: -75, opacity: 0 },
      description: { y: 75, opacity: 0 },
    },
    "variant-3": {
      title: { x: 75, opacity: 0 },
      tags: { y: 75, opacity: 0 },
      description: { x: 75, opacity: 0 },
    },
  };

  function getDefaultClipPath(previewElement) {
    for (const variant in defaultClipPaths) {
      if (previewElement.classList.contains(variant)) {
        return defaultClipPaths[variant];
      }
    }
    return "polygon(100% 0%, 0% 0%, 0% 100%, 100% 100%)";
  }

  function applyVariantStyles(previewElement) {
    const variant = previewElement.className
      .split(" ")
      .find((className) => className.startsWith("variant-"));
    if (variant && variantTransforms[variant]) {
      Object.entries(variantTransforms[variant]).forEach(
        ([elementClass, transform]) => {
          const element = previewElement.querySelector(
            `.preview-${elementClass}`
          );
          if (element) {
            gsap.set(element, transform);
          }
        }
      );
    }
  }

  function changeBg(newImgSrc) {
    const newImg = document.createElement("img");
    newImg.src = newImgSrc;
    newImg.style.position = "absolute";
    newImg.style.top = "0";
    newImg.style.left = "0";
    newImg.style.width = "100%";
    newImg.style.height = "100%";
    newImg.style.objectFit = "cover";
    newImg.style.opacity = "0";

    previewBg.appendChild(newImg);

    gsap.to(newImg, { opacity: 1, duration: 0.5 });

    if (previewBg.children.length > 1) {
      const oldImg = previewBg.children[0];
      gsap.to(oldImg, {
        opacity: 0,
        duration: 0.5,
        onComplete: () => {
          previewBg.removeChild(oldImg);
        },
      });
    }
  }

  previews.forEach((preview, index) => {
    const previewElement = document.createElement("div");
    previewElement.className = `preview ${mapClasses[index]} preview-${
      index + 1
    }`;
    previewElement.innerHTML = `
   <div class="preview-img"><img src="${preview.img}" alt=""/></div>
   <div class="preview-title"><h1>${preview.title}</h1></div>
   <div class="preview-tags"><p>${preview.tags}</p></div>
   <div class="preview-description"><p>${preview.description}</p></div>
 `;
    container.appendChild(previewElement);
    applyVariantStyles(previewElement);
  });

  items.forEach((item, index) => {
    item.addEventListener("mouseenter", () => {
      isMouseOverItem = true;
      const newBg = `./static/assets/bg-${index + 1}.jpg`;
      changeBg(newBg);

      const newActivePreview = document.querySelector(`.preview-${index + 1}`);
      if (activePreview && activePreview !== newActivePreview) {
        const previousActivePreviewImg =
          activePreview.querySelector(".preview-img");
        const previousDefaultClipPath = getDefaultClipPath(activePreview);
        gsap.to(previousActivePreviewImg, {
          clipPath: previousDefaultClipPath,
          duration: 0.75,
          ease: "power3.out",
        });

        gsap.to(activePreview, {
          opacity: 0,
          duration: 0.3,
          delay: 0.2,
        });
        applyVariantStyles(activePreview, true);
      }
      gsap.to(newActivePreview, { opacity: 1, duration: 0.1 });
      activePreview = newActivePreview;

      const elementsToAnimate = ["title", "tags", "description"];
      elementsToAnimate.forEach((el) => {
        const element = newActivePreview.querySelector(`.preview-${el}`);
        if (element) {
          gsap.to(element, { x: 0, y: 0, opacity: 1, duration: 0.5 });
        }
      });

      const activePreviewImg = activePreview.querySelector(".preview-img");
      gsap.to(activePreviewImg, {
        clipPath: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
        duration: 1,
        ease: "power3.out",
      });
    });

    item.addEventListener("mouseleave", () => {
      isMouseOverItem = false;
      applyVariantStyles(activePreview, true);

      setTimeout(() => {
        if (!isMouseOverItem) {
          changeBg("./static/assets/prev.png");
          if (activePreview) {
            gsap.to(activePreview, { opacity: 0, duration: 0.1 });
            const defaultPreview = document.querySelector(".preview.default");
            gsap.to(defaultPreview, { opacity: 1, duration: 0.1 });
            activePreview = defaultPreview;

            const activePreviewImg =
              activePreview.querySelector(".preview-img");
            const defaultClipPath = getDefaultClipPath(activePreview);
            gsap.to(activePreviewImg, {
              clipPath: defaultClipPath,
              duration: 1,
              ease: "power3.out",
            });
          }
        }
      }, 10);
    });
  });
});
