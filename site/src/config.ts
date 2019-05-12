export namespace Config {
    export const API_SERVER = process.env.NOTIFY_API_SERVER || location.origin;
    export const WEB_SERVER = process.env.NOTIFY_WEB_SERVER || location.origin;
}