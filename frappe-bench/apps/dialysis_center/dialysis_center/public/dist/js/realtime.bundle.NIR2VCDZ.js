(() => {
  var __defProp = Object.defineProperty;
  var __getOwnPropSymbols = Object.getOwnPropertySymbols;
  var __hasOwnProp = Object.prototype.hasOwnProperty;
  var __propIsEnum = Object.prototype.propertyIsEnumerable;
  var __defNormalProp = (obj, key, value) => key in obj ? __defProp(obj, key, { enumerable: true, configurable: true, writable: true, value }) : obj[key] = value;
  var __spreadValues = (a, b) => {
    for (var prop in b || (b = {}))
      if (__hasOwnProp.call(b, prop))
        __defNormalProp(a, prop, b[prop]);
    if (__getOwnPropSymbols)
      for (var prop of __getOwnPropSymbols(b)) {
        if (__propIsEnum.call(b, prop))
          __defNormalProp(a, prop, b[prop]);
      }
    return a;
  };

  // ../dialysis_center/dialysis_center/public/src/store/session-store.js
  var SessionStore = class {
    constructor() {
      this.sessions = [];
      this.listeners = [];
      this.loadFromCache();
    }
    getAll() {
      return this.sessions;
    }
    getById(sessionId) {
      return this.sessions.find((s) => s.name === sessionId);
    }
    upsert(session) {
      const index = this.sessions.findIndex((s) => s.name === session.name);
      if (index >= 0) {
        this.sessions[index] = __spreadValues(__spreadValues({}, this.sessions[index]), session);
      } else {
        this.sessions.push(session);
      }
      this.saveToCache();
      this.notify("session_updated", session);
    }
    remove(sessionId) {
      const index = this.sessions.findIndex((s) => s.name === sessionId);
      if (index >= 0) {
        const removed = this.sessions.splice(index, 1)[0];
        this.saveToCache();
        this.notify("session_removed", removed);
      }
    }
    updateVitals(sessionId, vitals) {
      const session = this.getById(sessionId);
      if (session) {
        if (!session.vitals) {
          session.vitals = [];
        }
        session.vitals.push(vitals);
        session.latest_vitals = vitals;
        this.saveToCache();
        this.notify("vitals_updated", { session: sessionId, vitals });
      }
    }
    clear() {
      this.sessions = [];
      this.saveToCache();
      this.notify("sessions_cleared");
    }
    subscribe(callback) {
      this.listeners.push(callback);
      return () => {
        const index = this.listeners.indexOf(callback);
        if (index >= 0) {
          this.listeners.splice(index, 1);
        }
      };
    }
    notify(event, data) {
      this.listeners.forEach((listener) => {
        try {
          listener(event, data);
        } catch (error) {
          console.error("Store listener error:", error);
        }
      });
    }
    saveToCache() {
      try {
        localStorage.setItem("dialysis_center_sessions", JSON.stringify(this.sessions));
      } catch (error) {
        console.error("Failed to save to cache:", error);
      }
    }
    loadFromCache() {
      try {
        const cached = localStorage.getItem("dialysis_center_sessions");
        if (cached) {
          this.sessions = JSON.parse(cached);
        }
      } catch (error) {
        console.error("Failed to load from cache:", error);
        this.sessions = [];
      }
    }
    getByStatus(status) {
      return this.sessions.filter((s) => s.status === status);
    }
    getCount() {
      return this.sessions.length;
    }
    getStats() {
      return {
        total: this.sessions.length,
        in_progress: this.sessions.filter((s) => s.status === "In Progress").length,
        scheduled: this.sessions.filter((s) => s.status === "Scheduled").length,
        completed: this.sessions.filter((s) => s.status === "Completed").length
      };
    }
  };
  window.sessionStore = new SessionStore();
  var session_store_default = window.sessionStore;

  // ../dialysis_center/dialysis_center/public/src/realtime/session-updates.js
  var RealtimeSessionHandler = class {
    constructor() {
      this.connected = false;
      this.init();
    }
    init() {
      if (!frappe.realtime) {
        console.warn("Frappe realtime not available");
        return;
      }
      this.setupEventListeners();
      this.connected = true;
      console.log("\u2705 Real-time session updates enabled");
    }
    setupEventListeners() {
      frappe.realtime.on("session_created", (data) => {
        console.log("Session created:", data);
        session_store_default.upsert(data.session);
        this.showNotification("New Session", `Session started for ${data.session.patient_name}`);
      });
      frappe.realtime.on("session_updated", (data) => {
        console.log("Session updated:", data);
        session_store_default.upsert(data.session);
      });
      frappe.realtime.on("session_completed", (data) => {
        console.log("Session completed:", data);
        session_store_default.upsert(data.session);
        this.showNotification("Session Completed", `Session for ${data.session.patient_name} completed`);
        setTimeout(() => {
          session_store_default.remove(data.session.name);
        }, 5e3);
      });
      frappe.realtime.on("vital_signs_added", (data) => {
        console.log("Vital signs added:", data);
        session_store_default.updateVitals(data.session, data.vitals);
        this.checkVitalAlerts(data.vitals, data.session);
      });
      frappe.realtime.on("session_event_logged", (data) => {
        console.log("Session event:", data);
        if (data.event.event_type === "Complication") {
          this.showNotification(
            "\u26A0\uFE0F Complication Alert",
            `${data.event.description} - Session: ${data.session}`,
            "orange"
          );
        }
      });
      frappe.realtime.on("machine_status_changed", (data) => {
        console.log("Machine status changed:", data);
        if (data.status === "Out of Service") {
          this.showNotification(
            "Machine Alert",
            `Machine ${data.machine} is out of service`,
            "red"
          );
        }
      });
      frappe.realtime.on("appointment_checked_in", (data) => {
        console.log("Appointment checked in:", data);
        this.showNotification(
          "Patient Checked In",
          `${data.patient_name} checked in`,
          "green"
        );
      });
    }
    checkVitalAlerts(vitals, sessionName) {
      const alerts = [];
      if (vitals.systolic_bp > 140 || vitals.systolic_bp < 90) {
        alerts.push(`Abnormal systolic BP: ${vitals.systolic_bp} mmHg`);
      }
      if (vitals.diastolic_bp > 90 || vitals.diastolic_bp < 60) {
        alerts.push(`Abnormal diastolic BP: ${vitals.diastolic_bp} mmHg`);
      }
      if (vitals.heart_rate > 100 || vitals.heart_rate < 60) {
        alerts.push(`Abnormal heart rate: ${vitals.heart_rate} bpm`);
      }
      if (vitals.temperature && (vitals.temperature > 37.5 || vitals.temperature < 36)) {
        alerts.push(`Abnormal temperature: ${vitals.temperature}\xB0C`);
      }
      if (alerts.length > 0) {
        this.showNotification(
          "\u26A0\uFE0F Vital Signs Alert",
          alerts.join(", ") + ` - Session: ${sessionName}`,
          "orange"
        );
      }
    }
    showNotification(title, message, indicator = "blue") {
      frappe.show_alert({
        message: `<strong>${title}</strong><br>${message}`,
        indicator
      }, 5);
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification(title, {
          body: message,
          icon: "/assets/dialysis_center/images/logo.png",
          badge: "/assets/dialysis_center/images/badge.png"
        });
      }
    }
    async requestNotificationPermission() {
      if ("Notification" in window && Notification.permission === "default") {
        const permission = await Notification.requestPermission();
        return permission === "granted";
      }
      return false;
    }
    emit(event, data) {
      if (frappe.realtime && frappe.realtime.socket) {
        frappe.realtime.socket.emit(event, data);
      }
    }
    disconnect() {
      this.connected = false;
      console.log("Real-time disconnected");
    }
  };
  window.realtimeSessionHandler = new RealtimeSessionHandler();
  var session_updates_default = window.realtimeSessionHandler;

  // ../dialysis_center/dialysis_center/public/src/realtime/notifications.js
  var NotificationManager = class {
    constructor() {
      this.notifications = [];
      this.maxNotifications = 50;
      this.init();
    }
    init() {
      this.loadFromStorage();
      this.requestPermission();
    }
    add(notification) {
      const notif = __spreadValues({
        id: this.generateId(),
        timestamp: new Date().toISOString(),
        read: false
      }, notification);
      this.notifications.unshift(notif);
      if (this.notifications.length > this.maxNotifications) {
        this.notifications = this.notifications.slice(0, this.maxNotifications);
      }
      this.saveToStorage();
      return notif;
    }
    markAsRead(notificationId) {
      const notif = this.notifications.find((n) => n.id === notificationId);
      if (notif) {
        notif.read = true;
        this.saveToStorage();
      }
    }
    markAllAsRead() {
      this.notifications.forEach((n) => n.read = true);
      this.saveToStorage();
    }
    getUnreadCount() {
      return this.notifications.filter((n) => !n.read).length;
    }
    getAll() {
      return this.notifications;
    }
    getUnread() {
      return this.notifications.filter((n) => !n.read);
    }
    clear() {
      this.notifications = [];
      this.saveToStorage();
    }
    saveToStorage() {
      try {
        localStorage.setItem("dialysis_center_notifications", JSON.stringify(this.notifications));
      } catch (error) {
        console.error("Failed to save notifications:", error);
      }
    }
    loadFromStorage() {
      try {
        const stored = localStorage.getItem("dialysis_center_notifications");
        if (stored) {
          this.notifications = JSON.parse(stored);
        }
      } catch (error) {
        console.error("Failed to load notifications:", error);
      }
    }
    async requestPermission() {
      if ("Notification" in window && Notification.permission === "default") {
        await Notification.requestPermission();
      }
    }
    showBrowserNotification(title, body, icon = null) {
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification(title, {
          body,
          icon: icon || "/assets/dialysis_center/images/logo.png",
          badge: "/assets/dialysis_center/images/badge.png",
          tag: this.generateId()
        });
      }
    }
    generateId() {
      return `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
  };
  window.notificationManager = new NotificationManager();
  var notifications_default = window.notificationManager;

  // ../dialysis_center/dialysis_center/public/src/realtime.bundle.js
  window.DialysisCenter = window.DialysisCenter || {};
  window.DialysisCenter.store = {
    sessionStore: session_store_default
  };
  window.DialysisCenter.realtime = {
    sessionHandler: session_updates_default,
    notifications: notifications_default
  };
  console.log("\u2705 Dialysis Center real-time system loaded");
})();
//# sourceMappingURL=realtime.bundle.NIR2VCDZ.js.map
