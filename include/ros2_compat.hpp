#pragma once
#include <rclcpp/rclcpp.hpp>
#include <builtin_interfaces/msg/time.hpp>
#include <cassert>
#include <cmath>
#include <type_traits>

inline double stamp_seconds(const builtin_interfaces::msg::Time &stamp) {
  return static_cast<double>(stamp.sec) + static_cast<double>(stamp.nanosec) * 1e-9;
}
inline builtin_interfaces::msg::Time stamp_from_seconds(double seconds) {
  return static_cast<builtin_interfaces::msg::Time>(rclcpp::Time(static_cast<int64_t>(std::llround(seconds * 1e9)), RCL_ROS_TIME));
}
namespace ros {
class NodeHandle {
public:
  explicit NodeHandle(const rclcpp::Node::SharedPtr &node) : node_(node) {}
  template<class T> void param(const std::string &name, T &out, const T &fallback) {
    std::string key = name;
    for (auto &c : key) if (c == '/') c = '.';
    if constexpr (std::is_same_v<T, float>) {
      out = static_cast<float>(node_->declare_parameter<double>(key, static_cast<double>(fallback)));
    } else {
      out = node_->declare_parameter<T>(key, fallback);
    }
  }
private:
  rclcpp::Node::SharedPtr node_;
};
}
