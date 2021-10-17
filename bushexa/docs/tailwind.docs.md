# Tailwindcss

Tailwindcss는 utility first css framework로 다른 css 프레임워크와는 다르게 utility를 최우선으로 삼습니다
코드를 예시로 tailwindcss가 어떤 css 프레임워크인지 살펴봅시다

```html
<div class="flex justify-center items-center bg-purple-500 rounded-lg shadow-md"></div>
```

위 코드에서 각 클래스네임들은 다음과 같은 css 속성을 가지고 있습니다

```css
/* static/src/styles.css */
.flex {
    display: flex;
}

.justify-center {
    justify-content: center;
}

.items-center {
    align-items: center;
}

.bg-purple-500 {
    --tw-bg-opacity: 1;
    background-color: rgba(139, 92, 246, var(--tw-bg-opacity));
}

.rounded-lg {
    border-radius: 0.5rem/* 8px */;
}

.shadow-md {
    --tw-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    box-shadow: var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000), var(--tw-shadow);
}
```

html 태그에 들어가는 클래스가 너무 길다고 생각하면 다음과 같이 변경할 수도 있습니다

```html
<div class="custom-card"><div>
```

```pcss
/* static/src/styles.pcss */
@tailwind base;
@tailwind components;

.custom-card {
    @apply flex justify-center items-center bg-purple-500 rounded-lg shadow-md;
}

@tailwind utilities;
```

tailwindcss는 다른 css 프레임워크처럼 클래스네임을 이용해 스타일링을 한다는 공통점이 있는 한편,
하나의 완성된 스타일 프리셋을 제공하는 것이 아니기 때문에 보다 자유롭게 UI디자인을 할 수 있다는 장점이 있습니다

tailwindcss 파일을 css파일로 만들고 싶다면 아래의 단계들을 따릅니다

1. node && npm 설치

2. bushexa폴더에서 다음을 실행

```bash
npm i # 이는 처음에만 실행하면 됩니다. node_modules를 install 하는 작업입니다
npm run buildcss # 이 커맨드는 html에 tailwind와 관련된 클래스네임을 변경하였을 때 이를 적용하기 위해 사용합니다
```
