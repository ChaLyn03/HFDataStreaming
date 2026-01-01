export interface Alert {
  id: string;
  signal_id: string;
  station_id: string;
  severity: string;
  alert_type: string;
  message: string;
  created_at: string;
}

export interface Signal {
  id: string;
  station_id: string;
  frequency_hz: number;
  snr_db: number;
  power_dbm?: number;
  band: string;
  timestamp: string;
  lat?: number;
  lon?: number;
}

export interface StatsSummary {
  station_id: string;
  count: number;
  avg_snr: number;
  alert_count: number;
}
