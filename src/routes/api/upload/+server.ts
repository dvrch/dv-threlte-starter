import { handleUpload, type HandleUploadBody } from '@vercel/blob/client';
import { json, type RequestEvent } from '@sveltejs/kit';

declare const process: any;

const BLOB_READ_WRITE_TOKEN = import.meta.env.VITE_BLOB_READ_WRITE_TOKEN || process.env.BLOB_READ_WRITE_TOKEN;

export async function POST({ request }: RequestEvent) {
    const body = (await request.json()) as HandleUploadBody;

    try {
        const jsonResponse = await handleUpload({
            body,
            request,
            token: BLOB_READ_WRITE_TOKEN,
            onBeforeGenerateToken: async (pathname) => {
                // Authenticate the user here if needed.
                // For now, we allow anyone to upload as requested implicitly by the unrestricted nature of the app so far,
                // (or we can add a check if the user is admin, but we have no auth context here easily yet).

                return {
                    allowedContentTypes: ['model/gltf-binary', 'model/gltf+json', 'application/octet-stream'],
                    tokenPayload: JSON.stringify({
                        // optional payload
                    }),
                };
            },
            onUploadCompleted: async ({ blob, tokenPayload }) => {
                console.log('blob upload completed', blob, tokenPayload);
                // We could notify the backend here, but we'll do it from the client for simplicity matching the current flow.
            },
        });

        return json(jsonResponse);
    } catch (error) {
        return json(
            { error: (error as Error).message },
            { status: 400 }
        );
    }
}
