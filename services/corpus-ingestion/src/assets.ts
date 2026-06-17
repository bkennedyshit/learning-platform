import {
  buildCorpusAssetKey,
  type ObjectStorageClient
} from "@learning-platform/object-storage";

export interface AssetRewriteResult {
  body: string;
  uploadedAssets: Array<{
    sourcePath: string;
    key: string;
    publicUrl: string;
  }>;
}

export interface AssetLoader {
  readAsset(path: string): Promise<{
    bytes: Uint8Array;
    contentType: string;
  }>;
}

const svgMarkdownPattern = /!\[([^\]]*)\]\(([^)]+\.svg)\)/gi;

export async function uploadAndRewriteSvgAssets(
  lessonId: string,
  body: string,
  loader: AssetLoader,
  storage: ObjectStorageClient
): Promise<AssetRewriteResult> {
  const uploadedAssets: AssetRewriteResult["uploadedAssets"] = [];
  let rewrittenBody = body;
  const matches = [...body.matchAll(svgMarkdownPattern)];

  for (const match of matches) {
    const fullMatch = match[0];
    const altText = match[1] ?? "";
    const sourcePath = match[2];
    if (!sourcePath) {
      continue;
    }

    const asset = await loader.readAsset(sourcePath);
    const key = buildCorpusAssetKey(lessonId, sourcePath.split(/[\\/]/).at(-1) ?? sourcePath);
    const stored = await storage.putObject({
      bucket: "corpus-assets",
      key,
      contentType: asset.contentType,
      body: asset.bytes
    });

    if (!stored.publicUrl) {
      throw new Error(`Uploaded asset ${sourcePath} has no public URL.`);
    }

    rewrittenBody = rewrittenBody.replace(fullMatch, `![${altText}](${stored.publicUrl})`);
    uploadedAssets.push({ sourcePath, key, publicUrl: stored.publicUrl });
  }

  return { body: rewrittenBody, uploadedAssets };
}
