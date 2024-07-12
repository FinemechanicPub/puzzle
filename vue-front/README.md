# Установка

## Рекоммендованные настроки IDE

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.vscode-typescript-vue-plugin).

## Конфигурирование

[Vite Configuration Reference](https://vitejs.dev/config/).

## Развертывание

### Установка зависимостей

```sh
npm install
```

### Компиляция и запуск сервера разработчика

```sh
npm run dev
```

### Компиляция и упаковка для развертывания

```sh
npm run build
```

## Заметки

### Адрес API

Устанавливается в переменной окружения `VITE_API_BASE_URI`, например:
```
VITE_API_BASE_URI=http://localhost:8000
```

Эта переменная доступна внутри приложения как
```javascript
import.meta.env.VITE_API_BASE_URI
```

### Автоматическая генерация клиентов API

Генерация кода по спецификации OpenAPI осуществляется с помощью пакета [@hey-api/openapi-ts](https://github.com/hey-api/openapi-ts). Для этого в [конфигурацию](package.json) введена команда `generate-client`:
```sh
npm run generate-client
```

Базовый путь API, который используют автоматически генерируемые клиенты, задаётся в [main.js](src/main.js):
```javascript
OpenAPI.BASE = `${import.meta.env.VITE_API_BASE_URI}`
```