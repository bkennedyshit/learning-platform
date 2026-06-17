import { Pool } from "pg";

export interface Database {
  pool: Pool;
  close(): Promise<void>;
}

const CONSISTENCY_WINDOW_MS = 2000;
const lastWrites = new Map<string, number>();

export function createDatabase(primaryUrl: string, replicaUrl?: string): Database {
  const primary = new Pool({ connectionString: primaryUrl });
  const replica = replicaUrl && replicaUrl !== primaryUrl ? new Pool({ connectionString: replicaUrl }) : primary;

  const poolProxy = new Proxy(primary, {
    get(target, prop, receiver) {
      if (prop === "query") {
        return async function(text: any, values?: any[]) {
          let queryText = "";
          if (typeof text === 'string') {
             queryText = text;
          } else if (text && typeof text.text === 'string') {
             queryText = text.text;
             if (!values && text.values) {
               values = text.values;
             }
          }
          
          let isWrite = false;
          if (queryText) {
             isWrite = /^\s*(insert|update|delete|with\s)/i.test(queryText);
          } else {
             isWrite = true;
          }

          let usePrimary = isWrite || primary === replica;

          if (!usePrimary && values && Array.isArray(values)) {
            const now = Date.now();
            for (const val of values) {
              if (typeof val === "string") {
                const lastWrite = lastWrites.get(val);
                if (lastWrite && now - lastWrite < CONSISTENCY_WINDOW_MS) {
                  usePrimary = true;
                  break;
                }
              }
            }
          }

          const pool = usePrimary ? primary : replica;
          const result = await pool.query(text, values);

          if (isWrite && values && Array.isArray(values)) {
            const now = Date.now();
            for (const val of values) {
              if (typeof val === "string") {
                lastWrites.set(val, now);
              }
            }
          }

          return result;
        };
      }
      
      if (prop === "connect") {
        return async function() {
           return await primary.connect();
        }
      }
      
      const val = Reflect.get(target, prop, receiver);
      if (typeof val === "function") {
        return val.bind(target);
      }
      return val;
    }
  });

  return {
    pool: poolProxy as Pool,
    close: async () => {
      await primary.end();
      if (primary !== replica) {
        await replica.end();
      }
    }
  };
}
