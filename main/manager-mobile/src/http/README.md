# Request library

The current project uses Alova as the only HTTP request library:

## Usage

- **Alova HTTP**: path (src/http/request/alova.ts)
- **Example code**: src/api/foo-alova.ts and src/api/foo.ts
- **API Documentation**: https://alova.js.org/

## Configuration instructions

Alova instance configured:
- Automatic Token authentication and refresh
- Unified error handling and prompts
- Support dynamic domain name switching
- Built-in request/response interceptor

## Usage example

```typescript
import { http } from '@/http/request/alova'

// GET request
http.Get<ResponseType>('/api/path', {
  params: { id: 1 },
  headers: { 'Custom-Header': 'value' },
meta: { toast: false } // Close error prompt
})

// POST request
http.Post<ResponseType>('/api/path', data, {
  params: { query: 'param' },
  headers: { 'Content-Type': 'application/json' }
})
```